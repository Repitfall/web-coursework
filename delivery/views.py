from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Ticket
from .serializers import UserSerializer, TicketSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
