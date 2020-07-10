from django.conf import settings
from rest_framework import serializers

from .models import Project, UserProject

MAX_DESCRIPTION_LENGTH = settings.MAX_DESCRIPTION_LENGTH
MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH
class ProjectSerializer(serializers.ModelSerializer):
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