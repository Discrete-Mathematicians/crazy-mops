from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("post/<int:post_pk>/new/", views.add_comment, name="create"),
    path("<int:comment_pk>/reply/", views.add_reply, name="reply"),
    path("<int:comment_pk>/delete/", views.delete_comment, name="delete"),
]
