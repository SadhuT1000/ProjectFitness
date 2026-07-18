from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    # Поля, которые будут отображаться в списке
    list_display = (
        "id",
        "avatar",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "tg_id",
        "is_staff",
        "is_active",
    )

    # Поля для поиска
    search_fields = ("email", "first_name", "last_name")

    # Фильтры справа
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Поля, используемые в форме редактирования
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Персональная информация", {"fields": ("first_name", "last_name", "phone_number", "avatar", "tg_id")}),
        ("Права доступа", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
