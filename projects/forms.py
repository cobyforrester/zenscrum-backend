from django import forms
from django.conf import settings
from .models import Project

MAX_DESCRIPTION_LENGTH = settings.MAX_DESCRIPTION_LENGTH
MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'begin_date', 'description', 'owner']

    #validate content
    def clean(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise forms.ValidationError('Description is over 120 characters')
        if len(title) > MAX_TITLE_LENGTH:
            raise forms.ValidationError('Title is over 30 characters')
        return self.cleaned_data