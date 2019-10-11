from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from .views import upload_data_sheet

app_name="ocr"

urlpatterns = [
    path('upload_data_sheet/',upload_data_sheet,name="upload_data_sheet"),
]