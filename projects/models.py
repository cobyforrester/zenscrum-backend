from datetime import date
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #many users can have many projects
    members = models.ManyToManyField(User, related_name='group_member', blank=True, through=UserProject) #to store list of people
    title = models.TextField(default='Title', blank=False, null=False)
    begin_date = models.DateField(default=date.today, blank=False, null=False)
    description = models.TextField(default='Description', blank=False, null=False)
    progress = models.BooleanField(default=True, null=False)

    class Meta:
        ordering = ['-id']
    def serialize(self):
        return{
            'id': self.id,
            'title': self.title,
            'begin_date': self.begin_date,
            'description': self.description,
            'user': self.user,
            'progress': self.progress
        }
    