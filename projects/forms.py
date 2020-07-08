from django import forms
from .models import Project

MAX_DESCRIPTION_LENGTH = 120
MAX_TITLE_LENGTH = 30

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