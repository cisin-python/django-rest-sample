"""Blog models managed here."""

from django.db import models
from django.contrib.auth.models import User
from registration.models import BaseModel
# from django.utils import timezone


class Feedback(BaseModel):
    """Feedbacks are managed here ."""

    TYPE = (
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="feeback")
    rating = models.IntegerField(default=0)
    content = models.TextField(default="")
    feedback_type = models.CharField(max_length=50, choices=TYPE, default="")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        """Model Representation."""
        return str(self.user)

    class Meta:
        """Class definition."""

        ordering = ['-updated_at']

    @classmethod
    def get_happy_students_record(cls):
        """Calculate the amount of happy students."""
        total_feedbacks = cls.objects.all().count()
        happy_feedbacks = cls.objects.filter(rating__gte=3).count()
        if total_feedbacks >= 1:
            percentage = (happy_feedbacks / total_feedbacks) * 100
        return happy_feedbacks, format(percentage, '.2f'), total_feedbacks


class Blog(BaseModel):
    """Blog model to manage blogs."""

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    author = models.CharField(max_length=20, default="Rank-Tree")
    title = models.CharField(max_length=200, null=True, blank=True)
    blog_content = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_blogs')
    image = models.FileField(max_length=250, upload_to="blog_images", blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Model Representation."""
        return str(self.blog_content)

    @property
    def like_counts(self):
        """Total number of likes of a particular blog."""
        return self.likes.all().count

    def react(self, user):
        """Perform like Unlike a blog."""
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
            react_type = "Like removed"
        else:
            self.likes.add(user)
            react_type = "Like added"
        return react_type

    class Meta:
        """Class definition."""

        ordering = ['-updated_at']
