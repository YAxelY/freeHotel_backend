from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Plan, HotelSubscription, Payment
from .serializers import PlanSerializer, HotelSubscriptionSerializer, PaymentSerializer
from hotels.models import Hotel
from reservations.models import Reservation
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .stripe_service import create_payment_intent, verify_webhook_signature
import json

# List all plans
class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]

# Create a payment for a hotel plan subscription
class PlanPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # Expected: hotel_id, plan_id, stripe_token, (user from request)
        hotel_id = request.data.get('hotel_id')
        plan_name = request.data.get('plan_name')
        stripe_token = request.data.get('stripe_token')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        plan = get_object_or_404(Plan, name=plan_name)
        user = request.user
        # Stripe payment logic would go here (stubbed)
        # Assume payment is successful for now
        with transaction.atomic():
            payment = Payment.objects.create(
                hotel=hotel,
                user=user,
                amount=plan.price,
                payment_type='plan',
                status='success',
                stripe_payment_id='test_stripe_id',
            )
            HotelSubscription.objects.create(
                hotel=hotel,
                plan=plan,
                is_active=True
            )
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

# Create a payment for a reservation
class ReservationPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # Expected: reservation_id, stripe_token, (user from request)
        reservation_id = request.data.get('reservation_id')
        stripe_token = request.data.get('stripe_token')
        reservation = get_object_or_404(Reservation, id=reservation_id)
        user = request.user
        hotel = reservation.room.hotel
        amount = reservation.room.price_per_night
        # Stripe payment logic would go here (stubbed)
        # Assume payment is successful for now
        payment = Payment.objects.create(
            hotel=hotel,
            reservation=reservation,
            user=user,
            amount=amount,
            payment_type='reservation',
            status='success',
            stripe_payment_id='test_stripe_id',
        )
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

# List all subscriptions (for hotelSubscriptions.jsx)
class HotelSubscriptionListView(generics.ListAPIView):
    queryset = HotelSubscription.objects.select_related('hotel', 'plan')
    serializer_class = HotelSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

# List all payments for a hotel or user
class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        hotel_id = self.request.query_params.get('hotel_id')
        if hotel_id:
            return Payment.objects.filter(hotel_id=hotel_id)
        return Payment.objects.filter(user=user)

# Cancel a plan (delete hotel and all related data)
class CancelPlanView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        hotel_id = request.data.get('hotel_id')
        reason = request.data.get('reason')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        # Delete all related data
        with transaction.atomic():
            hotel.delete()
        return Response({'detail': 'Plan cancelled and hotel deleted.'}, status=status.HTTP_200_OK)

class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'usd')
        metadata = request.data.get('metadata', {})
        payment_id = request.data.get('payment_id')
        if not amount:
            return Response({'error': 'Amount is required.'}, status=400)
        if not payment_id:
            return Response({'error': 'payment_id is required.'}, status=400)
        metadata['payment_id'] = str(payment_id)
        try:
            intent = create_payment_intent(float(amount), currency, metadata)
            return Response({'clientSecret': intent['client_secret']})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
        if not endpoint_secret:
            return Response({'error': 'Webhook secret not set.'}, status=500)
        try:
            event = verify_webhook_signature(payload, sig_header, endpoint_secret)
        except Exception as e:
            return Response({'error': f'Webhook error: {str(e)}'}, status=400)
        # Handle event types (expand as needed)
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            metadata = payment_intent.get('metadata', {})
            payment_id = metadata.get('payment_id')
            if payment_id:
                try:
                    payment = Payment.objects.get(id=payment_id)
                    payment.status = 'success'
                    payment.stripe_payment_id = payment_intent['id']
                    payment.save()
                except Payment.DoesNotExist:
                    pass  # Optionally log this
        return Response({'status': 'success'})
