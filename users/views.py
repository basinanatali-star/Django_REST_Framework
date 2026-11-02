from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from users.models import CustomUser, Payment
from users.serializers import UserSerializer, PaymentSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = [
        "paid_course",
        "paid_lesson",
        "payment_method",
    ]

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]