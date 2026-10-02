from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRegisterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        with transaction.atomic():
            event = get_object_or_404(Event.objects.select_for_update(), pk=pk)

            registration = Registration.objects.filter(
                user=request.user, event=event
            ).first()

            if registration and registration.status == Registration.Status.CONFIRMED:
                return Response(
                    {'detail': 'You are already registered for this event.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            taken = event.registrations.filter(
                status=Registration.Status.CONFIRMED
            ).count()
            if taken >= event.capacity:
                return Response(
                    {'detail': 'This event is full.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if registration:
                registration.status = Registration.Status.CONFIRMED
                registration.save()
                code = status.HTTP_200_OK
            else:
                registration = Registration.objects.create(
                    user=request.user, event=event
                )
                code = status.HTTP_201_CREATED

        return Response(RegistrationSerializer(registration).data, status=code)


class MyRegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(
            user=self.request.user
        ).select_related('event')


class RegistrationCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        registration = get_object_or_404(
            Registration, pk=pk, user=request.user
        )

        if registration.status == Registration.Status.CANCELLED:
            return Response(
                {'detail': 'This registration is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registration.status = Registration.Status.CANCELLED
        registration.save()
        return Response(RegistrationSerializer(registration).data)