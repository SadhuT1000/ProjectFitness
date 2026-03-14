from django.conf import settings
from django.db import models
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    class Meta:
        verbose_name = "Поток"
        verbose_name_plural = "Потоки"

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lesson(models.Model):
    """Модель урока внутри курса"""

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название урока"
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Ссылка на YouTube, Vimeo или другой хостинг"
    )
    week_number = models.PositiveIntegerField(
        verbose_name="Номер недели"
    )
    order = models.PositiveIntegerField(
        verbose_name="Порядковый номер урока"
    )
    is_free_preview = models.BooleanField(
        default=False,
        verbose_name="Бесплатный превью"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["week_number", "order"]

    def __str__(self):
        return f"{self.course.title} — Неделя {self.week_number} — {self.title}"


class Enrollment(models.Model):
    """Модель записи пользователя на поток (после оплаты)"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Пользователь"
    )
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Поток"
    )
    purchased_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата покупки"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    class Meta:
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курс"
        unique_together = ("user", "stream")  # нельзя купить один поток дважды

    def __str__(self):
        return f"{self.user} — {self.stream}"


class LessonProgress(models.Model):
    """Прогресс пользователя по урокам"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name="Пользователь"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name="Урок"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Пройден"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата прохождения"
    )

    class Meta:
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"
        unique_together = ("user", "lesson")  # один прогресс на урок на пользователя

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{status} {self.user} — {self.lesson.title}"