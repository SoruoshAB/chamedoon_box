from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

admin.site.site_header = "Chamedoon Admin Panel"
admin.site.unregister(Group)
admin.site.unregister(User)
