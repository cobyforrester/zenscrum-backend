from django.conf import settings
from rest_framework import serializers

from projects.models import Project
from .models import Sprint

MAX_GOAL_LENGTH = settings.MAX_GOAL_LENGTH
MIN_GOAL_LENGTH = settings.MIN_GOAL_LENGTH

#for posting data
class SprintSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'project', 'start_date', 'end_date', 'goal']

    #validate goal
    def validate_goal(self, value):
        if len(value) > MAX_GOAL_LENGTH:
            raise serializers.ValidationError('Goal is over ' + str(MAX_GOAL_LENGTH) +' characters')
        elif len(value) < MIN_GOAL_LENGTH:
            raise serializers.ValidationError('Goal must be at least '+ str(MIN_GOAL_LENGTH) + ' characters long')
        return value

#for posting data
class SprintSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'start_date', 'end_date', 'goal']

    #validate goal
    def validate_goal(self, value):
        if len(value) > MAX_GOAL_LENGTH:
            raise serializers.ValidationError('Goal is over ' + str(MAX_GOAL_LENGTH) +' characters')
        elif len(value) < MIN_GOAL_LENGTH:
            raise serializers.ValidationError('Goal must be at least '+ str(MIN_GOAL_LENGTH) + ' characters long')
        return value