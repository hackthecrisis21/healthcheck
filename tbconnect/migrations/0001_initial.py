# Generated by Django 3.1 on 2020-08-25 14:07

import functools
import uuid

import django.utils.timezone
from django.db import migrations, models

import userprofile.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TBCheck",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "deduplication_id",
                    models.CharField(default=uuid.uuid4, max_length=255, unique=True),
                ),
                (
                    "created_by",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                (
                    "msisdn",
                    models.CharField(
                        max_length=255,
                        validators=[
                            functools.partial(
                                userprofile.validators._phone_number,
                                *(),
                                **{"country": "ZA"}
                            )
                        ],
                    ),
                ),
                ("source", models.CharField(max_length=255)),
                (
                    "province",
                    models.CharField(
                        choices=[
                            ("ZA-EC", "Eastern Cape"),
                            ("ZA-FS", "Free State"),
                            ("ZA-GT", "Gauteng"),
                            ("ZA-LP", "Limpopo"),
                            ("ZA-MP", "Mpumalanga"),
                            ("ZA-NC", "Northern Cape"),
                            ("ZA-NL", "Kwazulu-Natal"),
                            ("ZA-NW", "North-West (South Africa)"),
                            ("ZA-WC", "Western Cape"),
                        ],
                        max_length=6,
                    ),
                ),
                ("city", models.CharField(max_length=255)),
                (
                    "age",
                    models.CharField(
                        choices=[
                            ("<18", "<18"),
                            ("18-40", "18-40"),
                            ("40-65", "40-65"),
                            (">65", ">65"),
                        ],
                        max_length=5,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                            ("not_say", "Rather not say"),
                        ],
                        max_length=7,
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        max_length=255,
                        validators=[userprofile.validators.geographic_coordinate],
                    ),
                ),
                (
                    "cough",
                    models.CharField(
                        choices=[
                            ("no", "No"),
                            ("yes_lt_2weeks", "Yes, less than 2 weeks"),
                            ("yes_gt_2weeks", "Yes, more than 2 weeks"),
                        ],
                        max_length=13,
                    ),
                ),
                ("fever", models.BooleanField()),
                ("sweat", models.BooleanField()),
                ("weight", models.BooleanField()),
                (
                    "exposure",
                    models.CharField(
                        choices=[
                            ("yes", "Yes"),
                            ("no", "No"),
                            ("not_sure", "Not sure"),
                        ],
                        max_length=9,
                    ),
                ),
                (
                    "tracing",
                    models.BooleanField(
                        help_text="Whether the NDoH can contact the user"
                    ),
                ),
                (
                    "completed_timestamp",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "risk",
                    models.CharField(
                        choices=[
                            ("low", "Low"),
                            ("moderate_without_cough", "Moderate without cough"),
                            ("moderate_with_cough", "Moderate with cough"),
                            ("high", "High"),
                        ],
                        max_length=22,
                    ),
                ),
            ],
        ),
    ]
