from django.urls import path

from posts import views

app_name = "posts"

urlpatterns = [
    path("new/<int:pet_pk>/", views.PostCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
]
