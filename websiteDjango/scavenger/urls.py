from django.urls import path
from . import views

urlpatterns = [
    path("", views.scavenger, name="scavenger")
]

