# Generated by Django 3.1 on 2020-12-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("selfswab", "0009_auto_20201130_0811"),
    ]

    operations = [
        migrations.AddField(
            model_name="selfswabscreen",
            name="should_sync",
            field=models.BooleanField(default=True),
        ),
    ]
