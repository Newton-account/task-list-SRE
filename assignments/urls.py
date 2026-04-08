from django.urls import path
from . import views

urlpatterns = [
    path('', views.assignment_list, name='assignment-list'),
    path('create/', views.assignment_create, name='assignment-create'),
    path('<int:pk>/update/', views.assignment_update, name='assignment-update'),
]