from django.urls import path
from user_profile import views

app_name = 'profile'

urlpatterns = [
    path('<int:pk>/', views.profile_detail, name='detail'),
]
