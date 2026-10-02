from rest_framework import serializers

from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    seats_available = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location',
            'date', 'capacity', 'seats_available', 'created_at',
        ]

    def get_seats_available(self, obj):
        taken = obj.registrations.filter(
            status=Registration.Status.CONFIRMED
        ).count()
        return obj.capacity - taken


class RegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'event', 'event_title', 'status', 'registered_at']