"""Blog app controller."""

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
    BlogSerializer, FeedbackListSerializer, FeedbackSerializer, BlogDetailSerializer,
    FeedbackContentOnlySerializer, CreateFeedbackSerilizer)
from .models import Blog, Feedback
from registration.utils import get_serializer_error
from registration.serializers import UserSerializer
from registration.models import PurchasedPackage
from student.models import AttemptedTestPackage


class BlogListAPIView(generics.ListAPIView):
    """API Controller to list all the blogs."""

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetailAPIView(generics.RetrieveAPIView):
    """Controller to get details of the perticular block."""

    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    # permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        """Update context."""
        context = super(BlogDetailAPIView, self).get_serializer_context()
        context.update({
            "user_id": self.request.query_params.get('user_id')
        })
        return context


class FeedbackListAPIView(generics.ListCreateAPIView):
    """API Controller to create and list all the feedbacks."""

    queryset = Feedback.objects.filter(is_active=True)
    serializer_class = FeedbackListSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Saving the feedback."""
        data = {
            'msg': "Successfully Created",
            'status': True,
            'feedback': {},
        }
        current_user = request.user
        context = {'current_user': current_user}
        serializer = FeedbackSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.validated_data['user'] = current_user
            feedback_obj = serializer.save(serializer.validated_data)
            data['feedback'] = FeedbackListSerializer(feedback_obj).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['msg'] = get_serializer_error(serializer.errors)
            data["status"] = False
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class FeedbackAPIView(generics.DestroyAPIView):
    """API Controller to delete a feedback."""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackListSerializer
    permission_classes = (IsAuthenticated,)


class LikeBlogAPIView(generics.ListCreateAPIView):
    """API Controller to manage likes on the blog."""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return the list of liked user of a specific blog."""
        try:
            blog = Blog.objects.get(id=self.kwargs.get('blog_pk'))
            return blog.likes.all()
        except Blog.DoesNotExist:
            return []

    def post(self, request, *args, **kwargs):
        """Performing like and unlike on block."""
        data = {
            'status': True,
        }
        current_user = request.user
        try:
            blog = Blog.objects.get(id=kwargs.get('blog_pk'))
            react_type = blog.react(current_user)
            data['msg'] = react_type
            return Response(data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            data['msg'] = "Blog not found"
            data['status'] = False
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CheckFeedbackExistanceAPIView(generics.GenericAPIView):
    """API Controller to list all the feedbacks."""

    queryset = []
    serializer_class = FeedbackContentOnlySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Saving the feedback."""
        data = {
            'msg': "Already exists",
            'status': True,
        }
        try:
            feedback = Feedback.objects.get(user=request.user)
            data['feedback'] = self.serializer_class(feedback).data
            return Response(data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            data['msg'] = "Feed does not exist with this user"
            data['status'] = False
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class FactsAPIView(generics.GenericAPIView):
    """API Controller to to calculate happy students based on feedbacks."""

    queryset = []
    serializer_class = FeedbackContentOnlySerializer

    def get(self, request):
        """Saving the feedback."""
        data = {}
        data['happy_feedbacks_count'], percentage, total_feedbacks = Feedback.get_happy_students_record()
        data['booked_packages_count'] = PurchasedPackage.objects.all().count()
        data['attempted_packages_count'] = AttemptedTestPackage.objects.all().count()
        return Response(data, status=status.HTTP_200_OK)


class CreateFeedbackAPIView(generics.GenericAPIView):
    """API to create feedback."""

    serializer_class = CreateFeedbackSerilizer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Create the feedback."""
        context = {'current_user': request.user}
        serializer = self.serializer_class(data=request.data, context=context)
        data = {
            'status': False,
        }
        if serializer.is_valid():
            data['status'] = True
            data['rating'] = serializer.validated_data.get('rating')
            data['content'] = serializer.validated_data.get('content')
            data['feedback_type'] = serializer.validated_data.get('feedback_type')
            return Response(data, status=status.HTTP_200_OK)
        else:
            data['msg'] = get_serializer_error(serializer.errors)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
