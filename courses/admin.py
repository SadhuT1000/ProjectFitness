from django.contrib import admin
from .models import Course, Stream, Lesson, Enrollment, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course Admin"""
    list_display = (
        'title',
        'base_price',
        'duration_minutes',
        'is_home',
        'is_gym',
        'is_published',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_home', 'is_gym', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'equipment')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description', 'duration_minutes',  # ← добавили
                'equipment', 'image', 'base_price', 'is_published'
            )
        }),
        ('Дополнительно', {
            'fields': ('is_home', 'is_gym', 'created_at', 'updated_at')
        }),
    )


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    """Stream Admin"""
    list_display = (
        'title',
        'course',
        'start_date',
        'end_date',
        'price',
        'status',
        'max_participants',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'start_date', 'end_date', 'course')
    search_fields = ('title', 'description', 'course__title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description', 'start_date', 'end_date', 'price', 'status', 'max_participants')
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Lesson Admin"""
    list_display = ('title', 'course', 'week_number', 'order', 'is_free_preview')
    list_filter = ('course', 'week_number', 'is_free_preview')
    search_fields = ('title', 'course__title')
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'video_url', 'is_free_preview')
        }),
        ('Порядок', {
            'fields': ('week_number', 'order')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Enrollment Admin"""
    list_display = ('user', 'stream', 'purchased_at', 'is_active')
    list_filter = ('is_active', 'purchased_at')
    search_fields = ('user__email', 'stream__title')
    readonly_fields = ('purchased_at',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """LessonProgress Admin"""
    list_display = ('user', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
    search_fields = ('user__email', 'lesson__title')
    readonly_fields = ('completed_at',)