"""All Question routes are managed here."""

from django.urls import path

from . import views

urlpatterns = [
    path('test-packages/', views.AllSubscriptionPackageAPIView.as_view(),
         name='All_test_packages'),
    path('test-package/<int:pk>/',
         views.SubscriptionDetailPackageAPIView.as_view(),
         name='test_package_detail'),
    path('questions/', views.QuestionsListAPIView.as_view(),
         name='question_list'),
    path('question-set/<int:pk>/',
         views.QuestionSetDetailAPIView.as_view(), name='question_set'),
    path('question-sets/', views.QuestionSetListAPIView.as_view(),
         name='question_set_list'),
    path('question-set/<int:package_id>/questions/',
         views.QuestionSetQuestionListAPIView.as_view(),
         name='question_list_by_set'),
    path('question-set/<int:pk>/dates/',
         views.QuestionSetDateListAPIView.as_view(),
         name='question_set_dates'),
    path('course-categories/', views.CourseCategoryListAPIView.as_view(),
         name='course_categories'),
    path('course-category/<int:pk>/test-packages/',
         views.SubscriptionPackageListByCategoryAPIView.as_view(),
         name='subscription_packages_by_category'),
    path('test-package/<int:pk>/questions/',
         views.GetSubscriptionPackageQuestionsAPIView.as_view(),
         name='test_package_questions'),
    path('search/course/',
         views.SearchingCourseListAPIView.as_view(),
         name='search-course'),
    path('test-package/<int:package_id>/questions-list/',
         views.TestPackageQuestionListAPIView.as_view(),
         name='question_list_by_test_package'),
]
