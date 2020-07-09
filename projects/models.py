from datetime import date
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    puser = models.ForeignKey(User, on_delete=models.CASCADE) #many users can have many projects
    title = models.TextField(default='Title', blank=False, null=False)
    begin_date = models.DateField(default=date.today, blank=False, null=False)
    description = models.TextField(default='Description', blank=False, null=False)
    owner = models.TextField(default='Owner', blank=True, null=False) # CHANGE TO NULL=FALSE
    progress = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ['-id'] #This makes the table in DESCENDING ORDER, default is ASC
    def serialize(self):
        return{
            'id': self.id,
            'title': self.title,
            'begin_date': self.begin_date,
            'description': self.description,
            'owner': self.owner,
            'progress': self.progress
        }
class UserProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    username_project = models.TextField(default='username', blank=False, null=False)
    