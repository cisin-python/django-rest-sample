"""Blog related Serializers are managed here."""
from rest_framework import serializers
from .models import Feedback, Blog
from registration.serializers import UserSerializer
from django.db import IntegrityError


class FeedbackListSerializer(serializers.ModelSerializer):
    """Serializer class for Feedback."""

    user_details = UserSerializer(source="user")

    class Meta():
        """Meta class."""

        model = Feedback
        fields = ['id', 'user_details', 'content', 'rating', 'is_active', 'feedback_type']


class FeedbackContentOnlySerializer(serializers.ModelSerializer):
    """Serializer class for Feedback Content only."""

    class Meta():
        """Meta class."""

        model = Feedback
        fields = ['id', 'content', 'rating', 'is_active', 'feedback_type']


class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer class for Feedback."""

    class Meta():
        """Meta class."""

        model = Feedback
        fields = ['id', 'rating', 'content', 'feedback_type']

    def validate(self, data):
        """Applying custom validations."""
        current_user = self.context.get('current_user')
        try:
            Feedback.objects.get(user=current_user)
            raise serializers.ValidationError("Feedback already exists")
        except Feedback.DoesNotExist:
            pass
        return data

    def save(self, val_data):
        """Creating a feedback."""
        try:
            feedback = Feedback.objects.create(**val_data)
        except IntegrityError:
            feedback = ""
        return feedback


class BlogSerializer(serializers.ModelSerializer):
    """Serializer class for Feedback."""

    blog_image = serializers.SerializerMethodField()

    class Meta():
        """Meta class."""

        model = Blog
        fields = ['id', 'title', 'blog_image', 'blog_content', 'like_counts']

    def get_blog_image(self, obj):
        """Getting custom field value."""
        try:
            image = obj.image.url
        except (ValueError):
            image = ""
        return image


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer class for Feedback."""

    blog_image = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        """Like status from the current user."""
        try:
            user_id = self.get_user()
            return obj.likes.filter(id=user_id).exists()
        except AttributeError:
            return False

    class Meta():
        """Meta class."""

        model = Blog
        fields = ['id', 'title', 'blog_image', 'blog_content', 'like_counts', 'is_liked', 'author', 'add_date']

    def get_blog_image(self, obj):
        """Getting custom field value."""
        try:
            image = obj.image.url
        except (ValueError):
            image = ""
        return image

    def get_user(self):
        """Get the current user id."""
        return self.context.get('user_id') if self.context.get('user_id') else 0


class CreateFeedbackSerilizer(serializers.Serializer):
    """Serializer class for create Feedback."""

    rating = serializers.IntegerField(required=True)
    content = serializers.CharField(required=True)
    feedback_type = serializers.CharField()

    def validate(self, data):
        """Saving the data."""
        current_user = self.context.get('current_user')
        try:
            feedback = Feedback.objects.get(user=current_user)
            raise serializers.ValidationError("Feedback already exists")
        except Feedback.DoesNotExist:
            current_user = self.context.get('current_user')
            rating = data.get('rating')
            content = data.get('content')
            feedback_type = data.get('feedback_type')
            feedback = Feedback.objects.create(user=current_user, rating=rating, content=content,
                                               feedback_type=feedback_type)
            feedback.save()
            return data
