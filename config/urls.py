"""config URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    # TODO: временная страница для проверки base.html
    path("test/", TemplateView.as_view(template_name="test_page.html")),
    path("login/", auth_views.LoginView.as_view(template_name="login_page.html"), name="login"),
    path("profile_edit/", TemplateView.as_view(template_name="profile_edit_page.html")),
    path("signup/", TemplateView.as_view(template_name="signup_page.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
