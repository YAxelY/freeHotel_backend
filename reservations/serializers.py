from rest_framework import serializers

from hotels.models import Room
from .models import Reservation
from hotels.serializers import RoomSerializer

class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        write_only=True  # Only for input, not output
    )
    room_details = RoomSerializer(source='room', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ('user', 'status', 'created_at', 'room_details')

    def validate(self, data):
        # Check if check_out is after check_in
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check-out must be after check-in")
        return data

    def create(self, validated_data):
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)