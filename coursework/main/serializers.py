from rest_framework import serializers
from .models import Users

class UsersSerialuzer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('role', 'first_name', 'last_name')