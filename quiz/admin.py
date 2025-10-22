from django.contrib import admin
from .models import Feedback, Question
# Register your models here.
from .models import GroupDiscussion
from .models import Institution
from .forms import InstitutionForm

@admin.register(GroupDiscussion)
class GroupDiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'link')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_title', 'username', 'rating')

admin.site.register(Feedback, FeedbackAdmin)


class InstitutionAdmin(admin.ModelAdmin):
    form = InstitutionForm
    list_display = ['name', 'contact', 'location', 'courses_provided']  # Corrected here
    search_fields = ['name', 'contact', 'location']  # Optional, for search functionality

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Question)

from .models import Notification

# Register the Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')  # Display the ID and text field in the admin list view
    search_fields = ('text',)  # Add search functionality for the text field

