from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_page, name="main_page"),
    path("save/", views.save_data, name="save_data_view"),

]