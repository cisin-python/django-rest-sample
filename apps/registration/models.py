# """Registration models managed here."""

# from django.db import models
# from django.contrib.auth.models import User
# # from django.db.models.signals import post_save
# # from .services import send_subadmin_email
# # import string
# # import random
# # from django.contrib import messages


# class BaseModel(models.Model):
#     """Base model for each models with common fields."""

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         """Abstract true."""

#         abstract = True


# class Profile(BaseModel):
#     """User profile model to manage profile."""

#     from question.models import Course
#     GENDER = (
#         ('male', 'Male'),
#         ('female', 'Female'),
#         ('not_specified', 'Not Specified'),
#     )
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name="profile")
#     image = models.ImageField(
#         upload_to="profile_images", blank=True, null=True)
#     full_name = models.CharField(blank=True, null=True, max_length=255)
#     phone_number = models.CharField(blank=True, null=True, max_length=255, unique=True)
#     gender = models.CharField(max_length=50, choices=GENDER, blank=True, null=True)
#     notification_batch = models.IntegerField(default=0)
#     id_proof = models.FileField(upload_to="id_proofs", blank=True, null=True)
#     is_approved = models.BooleanField(default=False)
#     is_mobile_verified = models.BooleanField(default=False)
#     is_email_verified = models.BooleanField(default=False)
#     is_camera_permission = models.BooleanField(default=False, blank=True, null=True)
#     resume = models.FileField(upload_to="resumes", blank=True, null=True)
#     secrete_token = models.UUIDField(blank=True, null=True)
#     otp_key = models.CharField(max_length=255, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     course = models.ManyToManyField(Course, related_name='courses')

#     def __str__(self):
#         """Object representation."""
#         return str(self.user)
