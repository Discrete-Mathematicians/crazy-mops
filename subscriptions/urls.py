from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("pets/<int:pet_pk>/subscribe/", views.subscribe, name="subscribe"),
    path("pets/<int:pet_pk>/unsubscribe/", views.unsubscribe, name="unsubscribe"),
]
