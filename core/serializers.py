from rest_framework import serializers

from core.models import *

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = '__all__'

class SheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shedule
        fields = '__all__'

class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo')

class ProjectSerializer(serializers.ModelSerializer):
    users_details = ShortUserSerializer(many=True, read_only=True, source='users')
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'users', 'users_details')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    shedules = SheduleSerializer(read_only=True, many=True, source='shedule_set')
    entries = EntrySerializer(read_only=True, many=True, source='entry_set')
    projects = ProjectSerializer(read_only=True, many=True, source='project_set',)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'status', 'comment', 'photo', 'shedules', 'entries', 'projects')

