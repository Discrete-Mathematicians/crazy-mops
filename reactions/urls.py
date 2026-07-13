from django.urls import path

from reactions import views

app_name = "reactions"
urlpatterns = [
    path("post/<int:post_pk>/", views.react_to_post, name="react_post"),
    path("comment/<int:comment_pk>/", views.react_to_comment, name="react_comment"),
]
