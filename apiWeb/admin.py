from django.contrib import admin

from .models import Slider

admin.site.site_header = "Chamedoon Admin Panel"

admin.site.register(Slider.SliderHome)
admin.site.register(Slider.SliderAds)
admin.site.register(Slider.SliderSong)
admin.site.register(Slider.SliderVideo)
