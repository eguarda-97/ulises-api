from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("temp_hum/", include("temp_hum.urls")),
]
