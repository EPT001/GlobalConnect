from django.urls import path
from . import views

app_name = 'profchat'
urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('update_user/', views.update_user, name='update_user'),
]