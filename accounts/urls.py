from django.urls import path
from rest_framework.documentation import include_docs_urls
from django.conf import settings

from .views import *

urlpatterns = [
    path('SendCodeToPhoneNumber', SendCodeToPhoneNumber.as_view()),
    path('VerifyPhoneNumberCodeApp', VerifyPhoneNumberCodeApp.as_view()),
    path('RefreshJwtToken', RefreshJwtToken.as_view()),
]
if settings.DEBUG:
    urlpatterns += [path(r'docs/Accountes/', include_docs_urls(title='Accountes'))]
