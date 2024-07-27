from django.urls import path
from . import views

app_name = 'comhub'
urlpatterns = [
    path('', views.home, name="comhub_home"),
    path('about/', views.about, name="comhub_about"),

    path('questions/', views.QuestionListView.as_view(), name="question_list"),
    # path('questions/new', views.QuestionCreateView.as_view(), name="question_create"),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('questions/add', views.add_question, name="add_question"),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name="question_update"),
    path('questions/<int:pk>/delete/', views.delete_question, name="delete_question"),
    path('questions/<int:pk>/comment/', views.AddCommentView.as_view(), name='question_comment'),
    path('like/<int:pk>/', views.like_view, name="like_post")   
]