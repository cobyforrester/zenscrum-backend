from django.conf import settings
from rest_framework import serializers

from .models import Project, UserProject

MAX_DESCRIPTION_LENGTH = settings.MAX_DESCRIPTION_LENGTH
MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH
PROJECT_MEMBERS_ACTION_OPTIONS = settings.PROJECT_MEMBERS_ACTION_OPTIONS

class ProjectActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in PROJECT_MEMBERS_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action for project members')
        return value

class ProjectSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'begin_date', 'description', 'progress']

    #validate description
    def validate_description(self, value):
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise serializers.ValidationError('Description is over 120 characters')
        return value

    #validate title
    def validate_title(self, value):
        if len(value) > MAX_TITLE_LENGTH:
            raise serializers.ValidationError('Description is over 120 characters')
        return value
class ProjectSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'begin_date', 'description', 'progress', 'user', 'members']