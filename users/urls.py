from django.urls import path
from users.views import PaymentViewSet
from django.urls import path, include
from rest_framework.routers import SimpleRouter

app_name = "users"

router = SimpleRouter()
router.register("payment", PaymentViewSet, basename="payment")


urlpatterns = [
    path("", include(router.urls)),
]
