from django.conf import settings
from rest_framework import serializers

from .models import Project, UserProject

MAX_DESCRIPTION_LENGTH = settings.MAX_DESCRIPTION_LENGTH
MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH
PROJECT_MEMBERS_ACTION_OPTIONS = settings.PROJECT_MEMBERS_ACTION_OPTIONS

class ProjectActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    member = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in PROJECT_MEMBERS_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action for project members')
        return value
#for posting data
class ProjectSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'begin_date', 'description']

    #validate description
    def validate_description(self, value):
        if len(value) > MAX_DESCRIPTION_LENGTH:
            raise serializers.ValidationError('Description is over 120 characters')
        elif len(value) == 0:
            raise serializers.ValidationError('Description required')
        return value

    #validate title
    def validate_title(self, value):
        if len(value) > MAX_TITLE_LENGTH or len(value) == 0:
            raise serializers.ValidationError('Description is over 120 characters')
        elif len(value) == 0:
            raise serializers.ValidationError('Title required')
        return value

#for viewing data
class ProjectSerializerGet(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'begin_date', 'description', 'progress', 'user', 'members'] #add members maybe?
    def get_members(self, obj):

        username = name = ''
        for i in obj.members.all():
            name += i.first_name + ' ' + i.last_name + ', '
            username += i.username + ', '

        data = {
                'name': name[:len(name) - 2],
                'username': username[:len(username) - 2],
            }
        
        return data

    def get_user(self, obj):
        data = {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'username': obj.user.username,
            }
        return data
