from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm

def assignment_list(request):
    assignments = Assignment.objects.select_related('student').all()
    return render(request, 'assignments/assignment_list.html', {
        'assignments': assignments,
    })

def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment created successfully!')
            return redirect('assignment-list')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_form.html', {
        'form': form,
        'title': 'Create Assignment',
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
    })