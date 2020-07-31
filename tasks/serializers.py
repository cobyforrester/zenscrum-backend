from django.conf import settings
from rest_framework import serializers

from projects.models import Project
from sprints.models import Sprint
from .models import Task

MAX_DESCRIPTION_LENGTH_TASK = settings.MAX_DESCRIPTION_LENGTH_TASK
MAX_TITLE_LENGTH_TASK = settings.MAX_TITLE_LENGTH_TASK
MIN_DESCRIPTION_LENGTH_TASK = settings.MIN_DESCRIPTION_LENGTH_TASK
MIN_TITLE_LENGTH_TASK = settings.MIN_TITLE_LENGTH_TASK

#for posting data
class TaskSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'sprint']

    #validate goal
    def validate_title(self, value):
        if len(value) > MAX_TITLE_LENGTH_TASK:
            raise serializers.ValidationError('Title is over ' + str(MAX_TITLE_LENGTH_TASK) +' characters')
        elif len(value) < MIN_TITLE_LENGTH_TASK:
            raise serializers.ValidationError('Title must be at least '+ str(MIN_TITLE_LENGTH_TASK) + ' characters long')
        return value
    def description(self, value):
        if len(value) > MAX_DESCRIPTION_LENGTH_TASK:
            raise serializers.ValidationError('Description is over ' + str(MAX_DESCRIPTION_LENGTH_TASK) +' characters')
        elif len(value) < MIN_DESCRIPTION_LENGTH_TASK:
            raise serializers.ValidationError('Description must be at least '+ str(MIN_DESCRIPTION_LENGTH_TASK) + ' characters long')
        return value

#for posting data
class TaskSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'start_date', 'title', 'description', 'completed']