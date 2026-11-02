from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import PaymentViewSet, UserViewSet, UserRegisterAPIView
from django.urls import path, include
from rest_framework.routers import SimpleRouter

app_name = "users"

router = SimpleRouter()
router.register("payment", PaymentViewSet, basename="payment")
router.register("users", UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
