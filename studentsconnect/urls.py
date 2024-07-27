from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import home, detail, posts

app_name = 'studentsconnect'
urlpatterns = [
path('', views.index, name='index'),
path('about/', views.about, name='about'),
path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
path('add_category/', views.add_category, name='add_category'),
path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
# path('register/', views.register, name='register'),
# path('login/', views.user_login, name='login'),
path('restricted/', views.restricted, name='restricted'),
# path('logout/', views.user_logout, name='logout'),
path('accounts/password/change/', PasswordChangeView.as_view(), name='auth_password_change'),
path('accounts/password/change/done/', PasswordChangeDoneView.as_view(), name='auth_password_change_done'),
# path('search/', views.search, name='search'),
path('', home, name="home"),
path('detail/', detail, name="detail"),
path('posts/', posts, name="posts"),
path('contact_admin/', views.contact_admin, name='contact_admin'),


]