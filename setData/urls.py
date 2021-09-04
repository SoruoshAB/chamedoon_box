from django.urls import path

from setData.views import verify_downloader, get_data, test_downloader


urlpatterns = [
    path('VerifyDownloader', verify_downloader.as_view()),
    path('TestDownloader', test_downloader.as_view()),
    path('VerifyDownloader', verify_downloader.as_view()),
    path('GetData', get_data.as_view()),
]