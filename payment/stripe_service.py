import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency='usd', metadata=None):
    """
    Create a Stripe PaymentIntent and return the client secret.
    Amount should be in dollars (Decimal or float), will be converted to cents.
    """
    if metadata is None:
        metadata = {}
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Stripe expects cents
        currency=currency,
        metadata=metadata,
        automatic_payment_methods={"enabled": True},
    )
    return intent

def verify_webhook_signature(payload, sig_header, endpoint_secret):
    """
    Verify the Stripe webhook signature and return the event object.
    """
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    return event 