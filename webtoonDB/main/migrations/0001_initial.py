# Generated by Django 4.1.3 on 2022-11-26 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Webtoon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=256)),
                (
                    "site",
                    models.CharField(
                        choices=[("AR", "AsuraScans"), ("MR", "MReader")],
                        default="MR",
                        max_length=2,
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        default="https://www.mreader.co/jumbo/manga/", max_length=1024
                    ),
                ),
                ("available_ch", models.FloatField(default=0)),
                ("finished_ch", models.FloatField(default=0)),
            ],
        ),
    ]
