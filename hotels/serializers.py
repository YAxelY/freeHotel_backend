from rest_framework import serializers
from .models import Hotel, Room, Review
from users.models import User
from payment.models import HotelSubscription

class RoomSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    hotel = serializers.SerializerMethodField(read_only=True)

    def get_hotel(self, obj):
        if obj.hotel:
            return {
                'id': obj.hotel.id,
                'name': obj.hotel.name,
                'logo_text': obj.hotel.logo_text,
                'location': obj.hotel.location,
                'rating': obj.hotel.rating,
                'template_data': obj.hotel.template_data,
                'status': obj.hotel.status,
                'description': obj.hotel.description,
                'amenities': obj.hotel.amenities,
            }
        return None

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_number', 'room_type', 'price_per_night',
            'capacity', 'is_available', 'image', 'last_booking'
        ]
        read_only_fields = ('hotel',)
        extra_kwargs = {
            'room_number': {'required': True},
            'room_type': {'required': False},
            'capacity': {'required': True},
            'is_available': {'required': False},
            'image': {'required': False},
        }

class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    owner_email = serializers.SerializerMethodField(read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    current_plan = serializers.SerializerMethodField(read_only=True)

    def get_owner_email(self, obj):
        # obj.owner is a HotelOwner instance, which has a .user (User) with .email
        if obj.owner and hasattr(obj.owner, 'user') and obj.owner.user:
            return obj.owner.user.email
        return None

    def get_current_plan(self, obj):
        sub = HotelSubscription.objects.filter(hotel=obj, is_active=True).order_by('-start_date').first()
        if sub:
            return {
                'name': sub.plan.name,
                'description': sub.plan.description,
                'price': str(sub.plan.price)
            }
        return None

    class Meta:
        model = Hotel
        fields = '__all__'
        extra_fields = ['owner_email', 'current_plan']
        read_only_fields = ('owner', 'owner_email', 'rating', 'published_at')

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    profile_photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'email', 'profile_photo', 'stars', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'username', 'email', 'created_at']

    def get_username(self, obj):
        return obj.user.username or ''

    def get_email(self, obj):
        return obj.user.email

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)