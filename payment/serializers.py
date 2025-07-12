from rest_framework import serializers
from .models import Plan, HotelSubscription, Payment

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class HotelSubscriptionSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    class Meta:
        model = HotelSubscription
        fields = ['id', 'hotel', 'hotel_name', 'plan', 'plan_name', 'start_date', 'end_date', 'is_active']

class PaymentSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'hotel', 'hotel_name', 'reservation', 'user', 'user_email', 'amount', 'payment_type', 'status', 'stripe_payment_id', 'created_at'] 