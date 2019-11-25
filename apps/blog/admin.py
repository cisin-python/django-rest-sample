"""Register your models here."""
from django.contrib import admin
from .models import Feedback, Blog


class FeedbackAdmin(admin.ModelAdmin):
    """FeedbackAdmin admin registration with certatin features."""

    list_display = ['id', 'user', 'rating', 'content', 'feedback_type', 'is_active']
    search_fields = ['user__username']
    list_filter = ['user__username']
    actions = ['accept_verification', 'deny_verification']
    list_select_related = ('user', )

    def accept_verification(self, request, queryset):
        """To accept the student feedback request."""
        feedback_id = queryset.filter().values_list("id", flat=True)
        Feedback.objects.filter(id__in=feedback_id).update(is_active=True)
    accept_verification.short_description = "Accept selected feedbacks"

    def deny_verification(self, request, queryset):
        """To denied the student feedback request."""
        feedback_id = queryset.filter().values_list("id", flat=True)
        Feedback.objects.filter(id__in=feedback_id).update(is_active=False)
    deny_verification.short_description = "deny selected feedbacks"

admin.site.register(Feedback, FeedbackAdmin)


class BlogAdmin(admin.ModelAdmin):
    """BlogAdmin admin registration with certatin features."""

    readonly_fields = ['author']
    list_display = ['id', 'title', 'author', 'blog_content', 'image', 'add_date']
    search_fields = ['blog_content']
    list_filter = ['image']

admin.site.register(Blog, BlogAdmin)
