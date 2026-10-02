from django.urls import path

from .views import (
    EventDetailView,
    EventListView,
    EventRegisterView,
    MyRegistrationListView,
    RegistrationCancelView,
)

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/register/', EventRegisterView.as_view(), name='event-register'),
    path('registrations/', MyRegistrationListView.as_view(), name='my-registrations'),
    path('registrations/<int:pk>/cancel/', RegistrationCancelView.as_view(), name='registration-cancel'),
]