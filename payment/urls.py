from django.urls import path
from .views import (
    PlanListView, PlanPaymentView, ReservationPaymentView,
    HotelSubscriptionListView, PaymentHistoryView, CancelPlanView,
    CreatePaymentIntentView, StripeWebhookView
)

urlpatterns = [
    path('plans/', PlanListView.as_view(), name='plan-list'),
    path('pay/plan/', PlanPaymentView.as_view(), name='plan-payment'),
    path('pay/reservation/', ReservationPaymentView.as_view(), name='reservation-payment'),
    path('subscriptions/', HotelSubscriptionListView.as_view(), name='hotel-subscriptions'),
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('cancel_plan/', CancelPlanView.as_view(), name='cancel-plan'),
    path('create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
] 