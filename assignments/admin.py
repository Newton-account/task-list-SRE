from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'due_date', 'is_completed']
    list_filter = ['is_completed', 'due_date', 'student__course']
    search_fields = ['title', 'student__first_name', 'student__last_name']