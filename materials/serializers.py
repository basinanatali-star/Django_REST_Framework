from rest_framework import serializers
from materials.models import Course, Lesson
from materials.validators import validate_youtube_url
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url]
    )

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user

        if not user.is_authenticated:
            return False

        return Subscription.objects.filter(user=user, course=obj).exists()


    class Meta:
        model = Course
        fields = ['name', 'description', 'preview', 'lesson_count', "lessons", "owner", "is_subscribed" ]
        read_only_fields = ["owner"]

