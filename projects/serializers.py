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
#for posting data
class ProjectSerializerPost(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
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
#for viewing data
class ProjectSerializerGet(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'begin_date', 'description', 'progress', 'user', 'members'] #add members maybe?
    def get_members(self, obj):
        s = ''
        for i in obj.members.all():
            s += i.username + ', '
        return s[:len(s) - 2] #list of members returned, comma taken off

    def get_user(self, obj):
        name = obj.user.first_name + ' ' + obj.user.last_name
        if name == ' ':
            name = obj.user.username
        return name
