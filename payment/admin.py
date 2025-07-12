from django.contrib import admin
from .models import Plan, HotelSubscription, Payment

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')

class HotelSubscriptionInline(admin.TabularInline):
    model = HotelSubscription
    extra = 0

@admin.register(HotelSubscription)
class HotelSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active', 'start_date')
    search_fields = ('hotel__name', 'plan__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'reservation', 'amount', 'payment_type', 'status', 'stripe_payment_id', 'created_at')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('user__email', 'hotel__name', 'reservation__id', 'stripe_payment_id')


