from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django.conf import settings

from django_redis import get_redis_connection
from temba_client.v2 import TembaClient
import requests
from selfswab.models import SelfSwabRegistration, SelfSwabScreen, SelfSwabTest
from healthcheck import utils


@periodic_task(run_every=crontab(minute="*/5"))
def poll_meditech_api_for_results():
    r = get_redis_connection()
    if r.get("poll_meditech_api_for_results"):
        return
    with r.lock("poll_meditech_api_for_results", 1800):
        if (
            settings.MEDITECH_URL
            and settings.MEDITECH_USER
            and settings.MEDITECH_PASSWORD
            and settings.RAPIDPRO_URL
            and settings.SELFSWAB_RAPIDPRO_TOKEN
            and settings.SELFSWAB_RAPIDPRO_FLOW
        ):
            rapidpro = TembaClient(
                settings.RAPIDPRO_URL, settings.SELFSWAB_RAPIDPRO_TOKEN
            )

            barcodes = list(
                SelfSwabTest.objects.filter(
                    result=SelfSwabTest.Result.PENDING
                ).values_list("barcode", flat=True)
            )

            if len(barcodes) == 0:
                return "No test results to poll"

            response = requests.post(
                url=settings.MEDITECH_URL,
                headers={"Content-Type": "application/json"},
                json={"barcodes": barcodes},
                auth=(settings.MEDITECH_USER, settings.MEDITECH_PASSWORD),
            )
            response.raise_for_status()
            results = response.json()["results"]
            for result in results:
                test_result = result.get("result", SelfSwabTest.Result.ERROR)
                if test_result not in (SelfSwabTest.Result.PENDING, ""):
                    registration = (
                        SelfSwabTest.objects.filter(
                            barcode=result["barcode"],
                            result=SelfSwabTest.Result.PENDING,
                        )
                        .order_by("-timestamp")
                        .first()
                    )

                    if not registration:
                        continue

                    registration.set_result(test_result)

                    if result.get("collDateTime"):
                        registration.collection_timestamp = result.get("collDateTime")
                    if result.get("recvDateTime"):
                        registration.received_timestamp = result.get("recvDateTime")
                    if result.get("verifyDateTime"):
                        registration.authorized_timestamp = result.get("verifyDateTime")

                    rapidpro.create_flow_start(
                        urns=[f"whatsapp:{registration.msisdn}"],
                        flow=settings.SELFSWAB_RAPIDPRO_FLOW,
                        extra={
                            "result": registration.result,
                            "error": result.get("error"),
                            "barcode": result["barcode"],
                            "updated_at": registration.updated_at.strftime("%d/%m/%Y"),
                        },
                    )
                    registration.save()

    return "Finished syncing test results to Rapidpro"


@periodic_task(run_every=crontab(minute="*/5"))
def perform_etl():
    r = get_redis_connection()
    if r.get("perform_etl_selfswab"):
        return

    models = {
        "registrations": {
            "model": SelfSwabRegistration,
            "field": "updated_at",
            "filter": {"key": "should_sync", "value": True},
            "fields": {
                "id": "STRING",
                "contact_id": "STRING",
                "employee_number": "STRING",
                "facility": "STRING",
                "occupation": "STRING",
                "age": "STRING",
                "gender": "STRING",
                "opted_out": "BOOLEAN",
                "optout_reason": "STRING",
                "optout_timestamp": "TIMESTAMP",
                "timestamp": "TIMESTAMP",
                "updated_at": "TIMESTAMP",
            },
        },
        "screens": {
            "model": SelfSwabScreen,
            "field": "timestamp",
            "filter": {"key": "should_sync", "value": True},
            "fields": {
                "id": "STRING",
                "contact_id": "STRING",
                "msisdn": "STRING",
                "age": "STRING",
                "gender": "STRING",
                "facility": "STRING",
                "risk_type": "STRING",
                "timestamp": "TIMESTAMP",
                "occupation": "STRING",
                "employee_number": "STRING",
                "pre_existing_condition": "STRING",
                "cough": "BOOLEAN",
                "fever": "BOOLEAN",
                "shortness_of_breath": "BOOLEAN",
                "body_aches": "BOOLEAN",
                "loss_of_taste_smell": "BOOLEAN",
                "sore_throat": "BOOLEAN",
                "additional_symptoms": "BOOLEAN",
            },
        },
        "tests": {
            "model": SelfSwabTest,
            "field": "updated_at",
            "filter": {"key": "should_sync", "value": True},
            "fields": {
                "id": "STRING",
                "contact_id": "STRING",
                "msisdn": "STRING",
                "result": "STRING",
                "barcode": "STRING",
                "timestamp": "TIMESTAMP",
                "updated_at": "TIMESTAMP",
                "collection_timestamp": "TIMESTAMP",
                "received_timestamp": "TIMESTAMP",
                "authorized_timestamp": "TIMESTAMP",
            },
        },
    }

    with r.lock("perform_etl_selfswab", 1800):
        utils.sync_models_to_bigquery(
            settings.SELFSWAB_BQ_KEY_PATH, settings.SELFSWAB_BQ_DATASET, models
        )
