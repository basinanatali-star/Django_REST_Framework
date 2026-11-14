from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import PaymentViewSet, UserViewSet, UserRegisterAPIView
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from users.views import payment_success, payment_cancel, payment_status

app_name = "users"

router = SimpleRouter()
router.register("payment", PaymentViewSet, basename="payment")
router.register("users", UserViewSet, basename="user")


urlpatterns = [
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
    path("payment/status/", payment_status, name="payment_status"),

    path("", include(router.urls)),
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
