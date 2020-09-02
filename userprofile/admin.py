from django.contrib import admin
from django.core.paginator import Paginator
from django.db import OperationalError, connection, transaction
from django.utils.functional import cached_property

from userprofile.models import Covid19Triage, HealthCheckUserProfile


class ApproximatePaginator(Paginator):
    """
    Paginator that returns an approximate count if doing the real count takes too long
    A mix between:
    https://hakibenita.com/optimizing-the-django-admin-paginator
    https://wiki.postgresql.org/wiki/Count_estimate
    """

    @cached_property
    def count(self):
        cursor = connection.cursor()
        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute("SET LOCAL statement_timeout TO 50")
            try:
                return super().count
            except OperationalError:
                pass
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT reltuples FROM pg_class WHERE relname = %s",
                [self.object_list.query.model._meta.db_table],
            )
            return int(cursor.fetchone()[0])


class BaseEventAdmin(admin.ModelAdmin):
    sortable_by = ()
    paginator = ApproximatePaginator
    show_full_result_count = False

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user.username
        super().save_model(request, obj, form, change)


@admin.register(Covid19Triage)
class Covid19TriageAdmin(BaseEventAdmin):
    readonly_fields = ("id", "created_by", "timestamp")
    list_display = ("msisdn", "risk", "source", "timestamp")


@admin.register(HealthCheckUserProfile)
class HealthCheckUserProfileAdmin(BaseEventAdmin):
    list_display = ("msisdn", "first_name", "gender")
