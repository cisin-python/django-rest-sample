"""Question app controller."""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    SubscriptionPackageListSerializer, QuestionSerializer,
    DateSlotSerializer, SubscriptionPackageAllQuestionSerializer,
    QuestionSetListSerializer, CategoryListSerializer,
    QuestionSetDetailSerializer, SubscriptionPackageDetailSerializer,
    AllsubjectiveQuestionSerializer,
    AllAudioQuestionListSerializer, TestPackageDetailSerializer,
    AllPassageQuestionListSerializer, AllTechnicalQuestionSerializer,
    SearchCourseSerializer, AllObjectiveQuestionSerializer)
from .models import SubscriptionPackage, QuestionSet, Question, CourseCategory, Course
from registration.models import PurchasedPackage
from rest_framework.response import Response
from rest_framework import status


class AllSubscriptionPackageAPIView(generics.ListCreateAPIView):
    """Controller to list all the subscription packages."""

    queryset = SubscriptionPackage.objects.filter(is_active=True)
    serializer_class = SubscriptionPackageListSerializer

    def get_queryset(self):
        """Custom Query set."""
        return SubscriptionPackage.objects.filter(
            question_set__course__name__icontains=self.request.query_params.get('name'), is_active=True)


class SubscriptionDetailPackageAPIView(generics.RetrieveAPIView):
    """Controller to get details of the subscription package."""

    queryset = SubscriptionPackage.objects.all()
    serializer_class = SubscriptionPackageDetailSerializer
    permission_classes = (IsAuthenticated,)


class QuestionsListAPIView(generics.ListCreateAPIView):
    """API Controller to list all the existing questions."""

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)


class QuestionSetDetailAPIView(generics.RetrieveAPIView):
    """API Controller to retrieve the particular question set."""

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetDetailSerializer
    permission_classes = (IsAuthenticated,)


class QuestionSetListAPIView(generics.ListAPIView):
    """API Controller to retrieve, update and delete the particular question set."""

    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetListSerializer
    permission_classes = (IsAuthenticated,)


class QuestionSetQuestionListAPIView(generics.ListAPIView):
    """API Controller to list all the questions of a particular question set."""

    serializer_class = AllObjectiveQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Getting custom data."""
        data = {}
        try:
            question_set = QuestionSet.objects.get(id=self.kwargs.get('package_id'))
            subscription_package = SubscriptionPackage.objects.get(
                question_set__id=self.kwargs.get('package_id')).name
            context = {
                'marks_per_objective_question': question_set.marks_per_objective_question,
                'marks_per_audio_question': question_set.marks_per_audio_question,
                'marks_per_passage_question': question_set.marks_per_passage_question,
                'marks_per_subjective_question': question_set.marks_per_subjective_question,
                'marks_per_technical_question': question_set.marks_per_technical_question,
            }
            question = question_set.questions()
        except QuestionSet.DoesNotExist:
            data['msg'] = 'invalid question_set id'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        try:
            test_package = self.request.user.purchased_packages.get(
                subscription_package__name=subscription_package)
        except PurchasedPackage.DoesNotExist:
            data['msg'] = 'invalid PurchasedPackage id'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        data['test_deatil'] = TestPackageDetailSerializer(test_package).data
        data['objective_questions'] = self.serializer_class(
            question['objective_questions'], many=True, context=context).data
        data['audio_questions'] = AllAudioQuestionListSerializer(
            question['audio_questions'], many=True, context=context).data
        data['passage_questions'] = AllPassageQuestionListSerializer(
            question['passage_questions'], many=True, context=context).data
        data['subjective_questions'] = AllsubjectiveQuestionSerializer(
            question['subjective_questions'], many=True, context=context).data
        data['technical_questions'] = AllTechnicalQuestionSerializer(
            question['technical_questions'], many=True, context=context).data
        return Response(data, status=status.HTTP_200_OK)


class QuestionSetDateListAPIView(generics.ListAPIView):
    """API Controller to List question set available dates."""

    serializer_class = DateSlotSerializer

    def get_queryset(self, *args, **kwargs):
        """Getting custom data."""
        try:
            question_set = QuestionSet.objects.get(id=self.kwargs.get('pk')).scheduled_time_slot.all()
            return question_set
        except QuestionSet.DoesNotExist:
            return []


class CourseCategoryListAPIView(generics.ListAPIView):
    """API Controller to List course categories."""

    queryset = []
    serializer_class = CategoryListSerializer

    def get(self, request):
        """API Controller to List course categories."""
        subject = request.query_params.get('subject')
        context = {}
        if subject:
            courses = CourseCategory.objects.filter(
                name__icontains=request.query_params.get('subject'))
            filtered_courses_id = courses.values_list('id')
            parents_id = list(filter(None, courses.values_list('parent', flat=True)))
            parent_categories = CourseCategory.objects.filter(pk__in=parents_id)
            context['filtered_courses_id'] = filtered_courses_id
        else:
            parent_categories = CourseCategory.objects.root_nodes()
        data = self.serializer_class(parent_categories, many=True, context=context).data
        return Response(data, status=status.HTTP_200_OK)


class SubscriptionPackageListByCategoryAPIView(generics.ListAPIView):
    """API Controller to List subscription packages by a course category."""

    serializer_class = SubscriptionPackageListSerializer

    def get_queryset(self):
        """List of subscription package by a particular course category."""
        return set(SubscriptionPackage.objects.filter(
            question_set__course__category=self.kwargs.get('pk')))


class GetSubscriptionPackageQuestionsAPIView(generics.RetrieveAPIView):
    """Controller to get details of the subscription package."""

    queryset = SubscriptionPackage.objects.all()
    serializer_class = SubscriptionPackageAllQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        """Update context."""
        context = super(
            GetSubscriptionPackageQuestionsAPIView, self).get_serializer_context()
        try:
            purchased_package = PurchasedPackage.objects.get(
                id=self.request.query_params.get('purchased_package_id'))
            context.update({
                "purchased_package": purchased_package,
            })
        except PurchasedPackage.DoesNotExist:
            pass
        return context


class SearchingCourseListAPIView(generics.ListAPIView):
    """API Controller to List course categories."""

    queryset = []
    serializer_class = SearchCourseSerializer

    def get(self, request):
        """API Controller to List course categories."""
        from itertools import chain
        subject = request.query_params.get('subject')
        context = {}

        if subject:
            parent_categories = CourseCategory.objects.filter(
                name__icontains=request.query_params.get('subject'))
            course_list = Course.objects.filter(name__icontains=subject)
            context['subject'] = subject
            context['filtered_courses_id'] = course_list.values_list('id')
            context['filtered_category_id'] = parent_categories.values_list('id')
            more_parent_categories = list(course.category for course in course_list)
            parent_categories = list(set(chain(parent_categories, more_parent_categories)))
        else:
            parent_categories = CourseCategory.objects.all()
        data = self.serializer_class(parent_categories, many=True, context=context).data
        return Response(data, status=status.HTTP_200_OK)


class TestPackageQuestionListAPIView(generics.ListAPIView):
    """API Controller to list all the questions of a particular question set."""

    serializer_class = AllObjectiveQuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """Getting custom data."""
        data = {}
        try:
            subscription_package = request.user.purchased_packages.get(
                id=self.kwargs.get('package_id')).subscription_package
            package_name = subscription_package.name
            question_set = subscription_package.question_set
            context = {
                'marks_per_objective_question': question_set.marks_per_objective_question,
                'marks_per_audio_question': question_set.marks_per_audio_question,
                'marks_per_passage_question': question_set.marks_per_passage_question,
                'marks_per_subjective_question': question_set.marks_per_subjective_question,
                'marks_per_technical_question': question_set.marks_per_technical_question,
            }
            question = question_set.questions()
        except PurchasedPackage.DoesNotExist:
            data['msg'] = 'Invalid Purchased Package id'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        purchased_packages = self.request.user.purchased_packages.filter(
            subscription_package__name=package_name)
        if purchased_packages:
            test_package = purchased_packages[0]
            # data['test_deatil'] = PurchasedSubscriptionPackageListSerializer(test_package).data
            data['test_deatil'] = TestPackageDetailSerializer(test_package).data
            data['objective_questions'] = self.serializer_class(
                question['objective_questions'], many=True, context=context).data
            data['audio_questions'] = AllAudioQuestionListSerializer(
                question['audio_questions'], many=True, context=context).data
            data['passage_questions'] = AllPassageQuestionListSerializer(
                question['passage_questions'], many=True, context=context).data
            data['subjective_questions'] = AllsubjectiveQuestionSerializer(
                question['subjective_questions'], many=True, context=context).data
            data['technical_questions'] = AllTechnicalQuestionSerializer(
                question['technical_questions'], many=True, context=context).data
        else:
            data['msg'] = 'there is no purchased_package avilable for this id'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)
