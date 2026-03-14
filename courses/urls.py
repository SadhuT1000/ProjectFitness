from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
    CourseCreateView, CourseDeleteView,
    CourseDetailView, CourseListView, CourseUpdateView,
    lesson_detail, mark_lesson_complete
)

app_name = "courses"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="courses_list"),
    path("courses/new/", CourseCreateView.as_view(), name="courses_create"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/update/<int:pk>/", CourseUpdateView.as_view(), name="courses_update"),
    path("courses/delete/<int:pk>/", CourseDeleteView.as_view(), name="courses_delete"),

    # Уроки
    path("courses/<int:course_pk>/lessons/<int:lesson_pk>/", lesson_detail, name="lesson_detail"),
    path("courses/<int:course_pk>/lessons/<int:lesson_pk>/complete/", mark_lesson_complete, name="lesson_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)