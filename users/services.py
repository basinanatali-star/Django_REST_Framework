import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(
        name=name,
    )
    return product.to_dict()


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe."""
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency="usd",
    )
    return price.to_dict()


def create_stripe_session(price_id):
    """Создание сессии оплаты в Stripe."""
    session = stripe.checkout.Session.create(
        success_url=(
            "http://127.0.0.1:8000/users/payment/success/"
            "?session_id={CHECKOUT_SESSION_ID}"
        ),
        cancel_url="http://127.0.0.1:8000/users/payment/cancel/",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return session.to_dict()


def retrieve_stripe_session(session_id):
    """Получение информации о сессии оплаты в Stripe."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.to_dict()
