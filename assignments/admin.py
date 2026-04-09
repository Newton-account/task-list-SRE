from django.contrib import admin

from .forms import AssignmentForm
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    form = AssignmentForm
    list_display = ['title', 'student', 'due_date', 'is_completed']
    list_filter = ['is_completed', 'due_date', 'student__course']
    search_fields = ['title', 'student__first_name', 'student__last_name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form_class = super().get_form(request, obj, change=change, **kwargs)
        is_add = obj is None

        class AdminAssignmentForm(form_class):
            def __init__(self, *args, **inner_kwargs):
                inner_kwargs['allow_bulk'] = False
                inner_kwargs['show_course_choice'] = is_add
                super().__init__(*args, **inner_kwargs)

        return AdminAssignmentForm

    def get_fields(self, request, obj=None):
        if obj is None:
            return ['course_choice', 'description', 'student', 'due_date', 'is_completed']
        return ['title', 'description', 'student', 'due_date', 'is_completed']

    def save_model(self, request, obj, form, change):
        if not change:
            course = form.cleaned_data.get('course_choice')
            if course is not None:
                obj.title = course.name

        super().save_model(request, obj, form, change)
