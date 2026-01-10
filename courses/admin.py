from django.contrib import admin
from .models import Course, Stream


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course Admin"""
    list_display = (
        'title',
        'base_price',
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
            'fields': ('title', 'description', 'equipment', 'image', 'base_price', 'is_published')
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



