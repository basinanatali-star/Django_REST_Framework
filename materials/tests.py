from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import Subscription


User = get_user_model()


class LessonTestCase(APITestCase):

    def setUp(self):
        # Создаём пользователей
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )

        self.user2 = User.objects.create_user(
            email="user2@test.com",
            password="testpass123"
        )

        self.moderator = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123"
        )

        # Создаём группу модераторов
        self.moderators_group, created = Group.objects.get_or_create(
            name="Модераторы"
        )
        self.moderator.groups.add(self.moderators_group)

        # Создаём курсы
        self.course = Course.objects.create(
            owner=self.user,
            name="Python",
            description="Курс по Python"
        )

        self.course2 = Course.objects.create(
            owner=self.user2,
            name="Django",
            description="Курс по Django"
        )

        # Создаём уроки
        self.lesson = Lesson.objects.create(
            owner=self.user,
            course=self.course,
            name="Основы Python",
            description="Первый урок",
            video_url="https://www.youtube.com/watch?v=example"
        )

        self.lesson2 = Lesson.objects.create(
            owner=self.user2,
            course=self.course2,
            name="Основы Django",
            description="Второй урок",
            video_url="https://www.youtube.com/watch?v=example"
        )

        # URL
        self.list_url = reverse("materials:lessons_list")
        self.create_url = reverse("materials:lessons_create")
        self.retrieve_url = reverse(
            "materials:lessons_retrieve",
            kwargs={"pk": self.lesson.pk}
        )
        self.update_url = reverse(
            "materials:lessons_update",
            kwargs={"pk": self.lesson.pk}
        )
        self.delete_url = reverse(
            "materials:lessons_delete",
            kwargs={"pk": self.lesson.pk}
        )

        self.subscription_url = reverse("materials:subscriptions")

        # Данные для создания урока
        self.lesson_data = {
            "course": self.course.pk,
            "name": "Новый урок",
            "description": "Описание нового урока",
            "video_url": "https://www.youtube.com/watch?v=example"
        }

    # ---------- CRUD УРОКОВ ----------

    def test_lesson_create(self):
        """Пользователь может создать урок."""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.create_url,
            self.lesson_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 3)

    def test_lesson_list(self):
        """Пользователь видит только свои уроки."""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_lesson_retrieve(self):
        """Пользователь может просмотреть свой урок."""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.retrieve_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Основы Python")

    def test_lesson_update(self):
        """Пользователь может изменить свой урок."""

        self.client.force_authenticate(user=self.user)

        data = {
            "course": self.course.pk,
            "name": "Изменённый урок",
            "description": "Новое описание",
            "video_url": "https://www.youtube.com/watch?v=example"
        }

        response = self.client.put(
            self.update_url,
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Изменённый урок")

    def test_lesson_delete(self):
        """Пользователь может удалить свой урок."""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Lesson.objects.filter(pk=self.lesson.pk).exists()
        )

    # ---------- ПРАВА ДОСТУПА ----------

    def test_user_cannot_access (self):
        """Пользователь не может просмотреть чужой урок."""

        self.client.force_authenticate(user=self.user)

        url = reverse(
            "materials:lessons_retrieve",
            kwargs={"pk": self.lesson2.pk}
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_view_all_lessons(self):
        """Модератор видит все уроки."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_moderator_can_update_lesson(self):
        """Модератор может изменить чужой урок."""

        self.client.force_authenticate(user=self.moderator)

        url = reverse(
            "materials:lessons_update",
            kwargs={"pk": self.lesson2.pk}
        )

        data = {
            "course": self.course2.pk,
            "name": "Изменено модератором",
            "description": "Новое описание",
            "video_url": "https://www.youtube.com/watch?v=example"
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson2.refresh_from_db()
        self.assertEqual(
            self.lesson2.name,
            "Изменено модератором"
        )

    def test_moderator_cannot_create_lesson(self):
        """Модератор не может создавать уроки."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.post(
            self.create_url,
            self.lesson_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_cannot_delete_lesson(self):
        """Модератор не может удалять уроки."""

        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_access_lessons(self):
        """Неавторизованный пользователь не имеет доступа."""

        response = self.client.get(self.list_url)

        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )

        self.user2 = User.objects.create_user(
            email="user2@test.com",
            password="testpass123"
        )

        self.course = Course.objects.create(
            owner=self.user,
            name="Python",
            description="Курс по Python"
        )

        self.subscription_url = reverse("materials:subscriptions")

        self.data = {
            "course_id": self.course.pk
        }

    def test_subscription_create(self):
        """Пользователь может подписаться на курс."""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            self.data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_subscription_delete(self):
        """Повторный запрос удаляет подписку."""

        Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            self.data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_subscription_is_individual(self):
        """Подписка одного пользователя не влияет на другого."""

        self.client.force_authenticate(user=self.user)

        self.client.post(self.subscription_url, self.data)

        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

        self.assertFalse(
            Subscription.objects.filter(
                user=self.user2,
                course=self.course
            ).exists()
        )

    def test_anonymous_cannot_subscribe(self):
        """Неавторизованный пользователь не может подписаться."""

        response = self.client.post(
            self.subscription_url,
            self.data
        )

        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])
