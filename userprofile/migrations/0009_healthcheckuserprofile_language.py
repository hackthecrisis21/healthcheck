# Generated by Django 3.1 on 2020-08-31 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0008_auto_20200820_1416"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthcheckuserprofile",
            name="language",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]