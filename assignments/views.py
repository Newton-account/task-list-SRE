from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from sudents.models import Student

from .models import Assignment
from .forms import AssignmentForm


def assignment_list(request):
    assignments = Assignment.objects.select_related('student').all()
    now = timezone.now()
    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
        'total_assignments': assignments.count(),
        'completed_assignments': assignments.filter(is_completed=True).count(),
        'pending_assignments': assignments.filter(is_completed=False).count(),
        'overdue_assignments': assignments.filter(is_completed=False, due_date__lt=now).count(),
        'now': now,
    })


def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, allow_bulk=True)
        if form.is_valid():
            assign_to = form.cleaned_data.get('assign_to')

            if assign_to == 'all':
                students = list(Student.objects.all())
                if not students:
                    form.add_error('assign_to', 'No students are available. Add students before assigning work to all.')
                else:
                    assignments = [
                        Assignment(
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            student=student,
                            due_date=form.cleaned_data['due_date'],
                            is_completed=form.cleaned_data['is_completed'],
                        )
                        for student in students
                    ]
                    Assignment.objects.bulk_create(assignments)
                    messages.success(request, f'Assignment created for all {len(students)} students.')
                    return redirect('assignment-list')
            else:
                form.save()
                messages.success(request, 'Assignment created successfully!')
                return redirect('assignment-list')
    else:
        form = AssignmentForm(allow_bulk=True)
    return render(request, 'assignments/assignment_form.html', {
        'form': form,
        'title': 'Create Assignment',
        'is_create': True,
    })


def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment-list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/assignment_form.html', {
        'form': form,
        'title': 'Update Assignment',
        'is_create': False,
    })
