# Generated by Django 3.1 on 2020-08-31 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tbconnect", "0003_tbcheck_follow_up_optin"),
    ]

    operations = [
        migrations.AddField(
            model_name="tbcheck",
            name="language",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
