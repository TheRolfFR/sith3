# Generated by Django 2.2.24 on 2021-11-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0036_auto_20211001_0248"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="pronouns",
            field=models.CharField(default="", max_length=64, verbose_name="pronouns"),
        ),
    ]
