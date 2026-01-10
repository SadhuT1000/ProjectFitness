from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from timeit import default_timer

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course, Stream



class CourseListView(ListView):
    """Список курсов"""
    model = Course
    template_name = "courses/courses_list.html"
    context_object_name = "courses"

class CourseCreateView(CreateView):
    """Создание курса"""
    model = Course
    template_name = "courses/course_form.html"
    fields = ["title", "description", "base_price", "is_published", "duration_minutes"]
    success_url = reverse_lazy("courses:courses_list")


class CourseDetailView(DeleteView):
    """Просмотр делатей курса"""
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = 'course'

class CourseUpdateView(UpdateView):
    """Внесение изменений в курс"""
    model = Course
    template_name = "courses/course_update.html"
    fields = ["title", "description", "base_price", "is_published"]
    success_url = reverse_lazy("courses:courses_list")


class CourseDeleteView(DeleteView):
    """Удаление курса"""
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("courses:courses_list")


