from django import forms
from .models import Project

MAX_DESCRIPTION_LENGTH = 500
MAX_TITLE_LENGTH = 30

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'begin_date', 'description', 'owner']

    #validate content
    def clean_content(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise forms.ValidationError('Description is over 500 characters')
        if len(title) > MAX_TITLE_LENGTH:
            raise forms.ValidationError('Title is over 500 characters')