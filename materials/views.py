from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsModeratorOrOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsModeratorOrOwner]
        else:
            permission_classes = [IsModeratorOrOwner]

        return [permission() for permission in permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in [
            "list",
            "retrieve",
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [IsModeratorOrOwner]
        else:
            permission_classes = [IsModeratorOrOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)