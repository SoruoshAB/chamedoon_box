from django.db import models

from .video import Videos


class Ads(models.Model):
    ad_id = models.PositiveIntegerField(primary_key=True, unique=True)
    image_url = models.TextField()
    click_url = models.TextField()
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, null=True, blank=True)
    is_video_ads = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Ads"

    def __str__(self):
        return str(self.ad_id)
