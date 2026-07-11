"""config URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("pets/", include("pets.urls")),
    path("profile/", include("user_profile.urls")),
    path("search/", include("search.urls")),
    path("subscriptions/", include("subscriptions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
