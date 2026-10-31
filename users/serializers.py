from rest_framework import serializers
from users.models import Payment


# class CourseSerializer(serializers.ModelSerializer):
#     lesson_count = serializers.SerializerMethodField()
#
#     def get_lesson_count(self, obj):
#         return obj.lessons.count()
#
#     class Meta:
#         model = Course
#         fields = ['name', 'description', 'preview', 'lesson_count']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'