# Generated by Django 3.1 on 2020-11-26 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("selfswab", "0007_auto_20201111_0726"),
    ]

    operations = [
        migrations.AlterField(
            model_name="selfswabregistration",
            name="employee_number",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
