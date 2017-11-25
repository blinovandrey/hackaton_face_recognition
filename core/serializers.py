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

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    shedules = SheduleSerializer(many=True, source='shedule_set')
    entries = EntrySerializer(many=True, source='entry_set')
    projects = ProjectSerializer(many=True, source='project_set')
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'status', 'photo', 'shedules', 'entries', 'projects')
