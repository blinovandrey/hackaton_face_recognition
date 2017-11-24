from rest_framework import serializers

from core.models import *

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # token = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
