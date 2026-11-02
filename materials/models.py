from django.conf import settings
from django.db import models

class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )
    name = models.CharField(max_length=150, verbose_name="Название курса")
    description = models.TextField(max_length=255, verbose_name="Описание курса")
    preview = models.ImageField(
        upload_to="courses/",
        verbose_name="Превью",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )
    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(max_length=255, verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="lessons/",
        verbose_name="Превью",
        blank=True,
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на видео",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

