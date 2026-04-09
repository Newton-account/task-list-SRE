from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from assignments.models import Assignment
from .models import Student


def dashboard(request):
    now = timezone.now()
    students = Student.objects.all()
    assignments = Assignment.objects.select_related('student')

    total_students = students.count()
    total_assignments = assignments.count()
    completed_assignments = assignments.filter(is_completed=True).count()
    pending_assignments = total_assignments - completed_assignments
    overdue_assignments = assignments.filter(is_completed=False, due_date__lt=now).count()
    due_this_week = assignments.filter(
        is_completed=False,
        due_date__gte=now,
        due_date__lte=now + timedelta(days=7),
    ).count()
    completion_rate = round((completed_assignments / total_assignments) * 100) if total_assignments else 0

    upcoming_assignments = assignments.filter(is_completed=False).order_by('due_date')[:6]
    recent_students = students.order_by('-enrolled_on', '-id')[:5]

    return render(request, 'dashboard.html', {
        'total_students': total_students,
        'total_assignments': total_assignments,
        'completed_assignments': completed_assignments,
        'pending_assignments': pending_assignments,
        'overdue_assignments': overdue_assignments,
        'due_this_week': due_this_week,
        'completion_rate': completion_rate,
        'upcoming_assignments': upcoming_assignments,
        'recent_students': recent_students,
    })


def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(course__icontains=query)
        )
    return render(request, 'sudents/student_list.html', {
        'students': students,
        'query': query,
        'student_count': students.count(),
    })
