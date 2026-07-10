"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    # TODO: временная страница для проверки base.html
    path("test/", TemplateView.as_view(template_name="test_page.html")),
]
