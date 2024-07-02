# HELP ME GOD.
from django.urls import path
from app.views import simpleserver

urlpatterns = [
    path("api/hello/", simpleserver, name="server"),
]
