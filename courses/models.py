
from django.contrib.auth.models import User
from django.db import models
from typing import TYPE_CHECKING
from decimal import Decimal


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    duration_minutes = models.PositiveIntegerField(
        verbose_name="Продолжительность (в минутах)"
    )
    equipment = models.TextField(
        verbose_name="Оборудование",
        help_text="Например: коврик, гантели, резинки"
    )
    description = models.TextField(
        verbose_name="Описание курса"
    )
    is_home = models.BooleanField(
        default=True,
        verbose_name="Подходит для дома"
    )
    is_gym = models.BooleanField(
        default=False,
        verbose_name="Подходит для зала"
    )
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Базовая цена"
    )
    is_published = models.BooleanField(
        default=True, verbose_name="Опубликован"
    )
    image = models.ImageField(
        upload_to='courses/', blank=True, null=True, verbose_name="Обложка курса"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Stream(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        OPEN = "open", "Открыт"
        IN_PROGRESS = "in_progress", "Идёт"
        FINISHED = "finished", "Завершён"

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="streams"
    )

    title = models.CharField(
        max_length=100,
        verbose_name="Название потока"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание запуска"
    )

    start_date = models.DateField(
        verbose_name="Дата начала"
    )

    end_date = models.DateField(
        verbose_name="Дата окончания"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Цена потока"
    )

    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Лимит участников"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} — {self.title}"
