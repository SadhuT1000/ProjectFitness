from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Course, Stream, Lesson, Enrollment, LessonProgress


class StaffRequiredMixin(UserPassesTestMixin):
    """Доступ только для staff"""
    def test_func(self):
        return self.request.user.is_staff


class CourseListView(ListView):
    """Список курсов"""
    model = Course
    template_name = "courses/courses_list.html"
    context_object_name = "courses"


class CourseCreateView(StaffRequiredMixin, CreateView):
    """Создание курса — только для staff"""
    model = Course
    template_name = "courses/course_form.html"
    fields = ["title", "description", "base_price", "is_published", "duration_minutes", "equipment", "is_home", "is_gym", "image"]
    success_url = reverse_lazy("courses:courses_list")


class CourseDetailView(DetailView):
    """Страница курса — описание, уроки, кнопка купить"""
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user

        # Открытые потоки курса
        context['open_streams'] = course.streams.filter(
            status=Stream.Status.OPEN
        )

        # Уроки курса
        context['lessons'] = course.lessons.all().order_by('week_number', 'order')

        # Есть ли у пользователя доступ к курсу
        context['has_access'] = False
        if user.is_authenticated:
            context['has_access'] = Enrollment.objects.filter(
                user=user,
                stream__course=course,
                is_active=True,
                stream__end_date__gte=timezone.now().date()
            ).exists()

        return context


class CourseUpdateView(StaffRequiredMixin, UpdateView):
    """Редактирование курса — только для staff"""
    model = Course
    template_name = "courses/course_update.html"
    fields = ["title", "description", "base_price", "is_published", "duration_minutes", "equipment", "is_home", "is_gym", "image"]
    success_url = reverse_lazy("courses:courses_list")


class CourseDeleteView(StaffRequiredMixin, DeleteView):
    """Удаление курса — только для staff"""
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("courses:courses_list")


@login_required
def lesson_detail(request, course_pk, lesson_pk):
    """Страница урока — только для купивших курс"""
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)

    # Проверяем доступ
    has_access = (
        lesson.is_free_preview or
        Enrollment.objects.filter(
            user=request.user,
            stream__course=course,
            is_active=True,
            stream__end_date__gte=timezone.now().date()
        ).exists()
    )

    if not has_access:
        return render(request, 'courses/no_access.html', {
            'course': course,
            'open_streams': course.streams.filter(status=Stream.Status.OPEN)
        })

    # Прогресс пользователя по этому уроку
    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    # Все уроки курса для навигации
    all_lessons = list(course.lessons.all().order_by('week_number', 'order'))
    current_index = next(
        (i for i, l in enumerate(all_lessons) if l.pk == lesson.pk), 0
    )

    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    # Прогресс по всему курсу
    total_lessons = len(all_lessons)
    completed_lessons = LessonProgress.objects.filter(
        user=request.user,
        lesson__course=course,
        is_completed=True
    ).count()
    percent = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'all_lessons': all_lessons,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'percent': percent,
    })


@login_required
def mark_lesson_complete(request, course_pk, lesson_pk):
    """Отметить урок как пройденный"""
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_pk)
        lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)

        has_access = (
            lesson.is_free_preview or
            Enrollment.objects.filter(
                user=request.user,
                stream__course=course,
                is_active=True,
                stream__end_date__gte=timezone.now().date()
            ).exists()
        )

        if not has_access:
            return HttpResponseForbidden()

        progress, _ = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

    return redirect('courses:lesson_detail', course_pk=course_pk, lesson_pk=lesson_pk)