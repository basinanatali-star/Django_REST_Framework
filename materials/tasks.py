from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Course
from users.models import Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправляет письмо пользователям, подписанным на обновления курса."""

    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return "Курс не найден"

    subscriptions = Subscription.objects.filter(
        course=course
    ).select_related("user")

    for subscription in subscriptions:
        user = subscription.user

        if user.email:
            send_mail(
                subject=f"Обновление курса: {course.name}",
                message=(
                    f"Здравствуйте, {user}!\n\n"
                    f"Курс «{course.name}» был обновлён.\n"
                    f"Описание курса: {course.description}\n\n"
                    "Зайдите на платформу, чтобы ознакомиться с обновлениями."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )