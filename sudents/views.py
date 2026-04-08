from django.db.models import Q
from django.shortcuts import render

from .models import Student


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
    })
