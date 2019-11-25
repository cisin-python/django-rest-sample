"""All Blog routes are managed here."""

from django.urls import path  # , include
from . import views

urlpatterns = [
    path('', views.BlogListAPIView.as_view(), name='blog_list'),
    path('<int:blog_pk>/react/', views.LikeBlogAPIView.as_view(), name='like_a_blog'),
    path('<int:pk>/detail/', views.BlogDetailAPIView.as_view(), name='Blog_detail'),
    path('feedbacks/', views.FeedbackListAPIView.as_view(), name='feedback_list'),
    path('feedback/create/', views.CreateFeedbackAPIView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/', views.FeedbackAPIView.as_view(), name='feedback_delete'),
    path('check-feedback-existance/', views.CheckFeedbackExistanceAPIView.as_view(), name='feedback_existance'),
    path('facts/', views.FactsAPIView.as_view(), name='happy_students_count'),
]
