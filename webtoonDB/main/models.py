from django.db import models

# Create your models here.


class Webtoon(models.Model):
    ASURA = "AR"
    MREADER = "MR"
    SITE_CHOICES = [
        (ASURA, "AsuraScans"),
        (MREADER, "MReader"),
    ]
    title = models.CharField(max_length=256)
    site = models.CharField(
        max_length=2,
        choices=SITE_CHOICES,
        default=MREADER,
    )
    url = models.URLField(
        max_length=1024,
        default="https://www.mreader.co/jumbo/manga/",
    )
    available_ch = models.FloatField(default=0)
    finished_ch = models.FloatField(default=0)

    def __str__(self) -> str:
        return self.title
