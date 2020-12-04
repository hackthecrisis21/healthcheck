# Generated by Django 3.1 on 2020-12-02 10:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("selfswab", "0011_selfswabtest_should_sync"),
    ]

    operations = [
        migrations.AddField(
            model_name="selfswabregistration",
            name="age",
            field=models.CharField(
                choices=[
                    ("<18", "<18"),
                    ("18-39", "18-39"),
                    ("40-65", "40-65"),
                    (">65", ">65"),
                ],
                max_length=5,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="selfswabregistration",
            name="gender",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Other", "Other"),
                    ("not_say", "not_say"),
                ],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="selfswabregistration",
            name="should_sync",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="selfswabregistration",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="selfswabregistration",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
    ]