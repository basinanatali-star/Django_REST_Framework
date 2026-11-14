import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from users.models import CustomUser, Payment
from users.serializers import UserSerializer, PaymentSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    retrieve_stripe_session,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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

    def perform_create(self, serializer):
        payment_method = serializer.validated_data["payment_method"]

        # Если оплата не через Stripe, сохраняем обычный платеж
        if payment_method != Payment.PaymentMethod.STRIPE:
            serializer.save(user=self.request.user)
            return

        paid_course = serializer.validated_data.get("paid_course")
        paid_lesson = serializer.validated_data.get("paid_lesson")

        # Указываем либо курс, либо урок
        if bool(paid_course) == bool(paid_lesson):
            raise ValidationError(
                "Укажите либо курс, либо урок для оплаты."
            )

        name = paid_course.name if paid_course else paid_lesson.name
        amount = serializer.validated_data["amount"]

        try:
            # Создаем продукт
            product = create_stripe_product(name)

            # Создаем цену
            price = create_stripe_price(product["id"], amount)

            # Создаем сессию оплаты
            session = create_stripe_session(price["id"])

        except stripe.StripeError as error:
            raise ValidationError({"stripe": str(error)})

        # Сохраняем платеж и ссылку на оплату
        serializer.save(
            user=self.request.user,
            payment_url=session["url"],
            stripe_session_id=session["id"],
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def payment_success(request):
    return Response({"message": "Оплата успешно завершена"})


@api_view(["GET"])
@permission_classes([AllowAny])
def payment_cancel(request):
    return Response({"message": "Оплата отменена"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_status(request):
    """Проверка статуса оплаты в Stripe."""

    session_id = request.query_params.get("session_id")

    if not session_id:
        return Response(
            {"error": "Не указан session_id"},
            status=400
        )

    try:
        payment = Payment.objects.get(
            stripe_session_id=session_id,
            user=request.user,
        )
    except Payment.DoesNotExist:
        return Response(
            {"error": "Платеж не найден"},
            status=404
        )

    try:
        session = retrieve_stripe_session(session_id)
    except stripe.StripeError as error:
        raise ValidationError({"stripe": str(error)})

    if session.get("payment_status") == "paid":
        payment.status = Payment.PaymentStatus.PAID
        payment.save(update_fields=["status"])

    return Response({
        "payment_id": payment.id,
        "stripe_session_id": session_id,
        "stripe_status": session.get("status"),
        "stripe_payment_status": session.get("payment_status"),
        "payment_status": payment.status,
    })