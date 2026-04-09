from django import forms

from sudents.models import Course

from .models import Assignment


class AssignmentForm(forms.ModelForm):
    ASSIGN_TO_CHOICES = [
        ('single', 'One student'),
        ('all', 'All students'),
    ]

    assign_to = forms.ChoiceField(
        choices=ASSIGN_TO_CHOICES,
        initial='single',
        help_text='Choose whether this assignment should be created for one student or everyone.',
    )
    course_choice = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=False,
        empty_label='Select course',
        help_text='Choose a registered course to use as the assignment title.',
    )
    due_date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(
            date_attrs={'type': 'date'},
            time_attrs={'type': 'time'},
        ),
        help_text='Select the date and time for the assignment deadline.',
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'student', 'due_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter assignment title'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Add instructions, expectations, or notes'}),
        }

    def __init__(self, *args, allow_bulk=False, show_course_choice=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.allow_bulk = allow_bulk
        self.show_course_choice = show_course_choice

        self.fields['course_choice'].queryset = Course.objects.all()

        self.fields['student'].required = False
        self.fields['student'].help_text = 'Pick a student when assigning to one person.'

        if self.allow_bulk:
            self.fields = {'assign_to': self.fields['assign_to'], **self.fields}
        else:
            self.fields.pop('assign_to')
            self.fields['student'].required = True
            self.fields['student'].help_text = 'Select the student for this assignment.'

        if not self.show_course_choice:
            self.fields.pop('course_choice')

    def clean(self):
        cleaned_data = super().clean()
        assign_to = cleaned_data.get('assign_to', 'single')
        student = cleaned_data.get('student')
        course_choice = cleaned_data.get('course_choice')

        if self.allow_bulk and assign_to == 'single' and not student:
            self.add_error('student', 'Select a student or switch the assignment target to all students.')

        if not self.allow_bulk and not student:
            self.add_error('student', 'Select a student for this assignment.')

        if self.show_course_choice and not course_choice:
            self.add_error('course_choice', 'Select a course for this assignment.')

        return cleaned_data
