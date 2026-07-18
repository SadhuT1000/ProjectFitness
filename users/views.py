from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages

from .forms import CustomUserCreationForm, ProfileUpdateForm
from courses.models import Enrollment, LessonProgress


# Регистрация
class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("landing:home")


# Вход
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


# Выход
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('landing:home')


# Личный кабинет
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        enrollments = (
            Enrollment.objects
            .filter(user=user, is_active=True)
            .select_related('stream', 'stream__course')
            .order_by('-purchased_at')
        )

        enrollments_with_progress = []
        for enrollment in enrollments:
            course = enrollment.stream.course
            total_lessons = course.lessons.count()
            completed_lessons = LessonProgress.objects.filter(
                user=user,
                lesson__course=course,
                is_completed=True
            ).count()

            percent = (
                int((completed_lessons / total_lessons) * 100)
                if total_lessons > 0 else 0
            )

            today = timezone.now().date()
            stream_active = enrollment.stream.end_date >= today

            enrollments_with_progress.append({
                'enrollment': enrollment,
                'course': course,
                'stream': enrollment.stream,
                'total_lessons': total_lessons,
                'completed_lessons': completed_lessons,
                'percent': percent,
                'stream_active': stream_active,
            })

        context['enrollments_with_progress'] = enrollments_with_progress
        context['user'] = user
        return context


# Редактирование профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile_edit.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


# Смена пароля
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён!')
        return super().form_valid(form)