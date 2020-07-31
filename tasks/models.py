from datetime import date
from django.db import models
from projects.models import Project
from sprints.models import Sprint

class Task(models.Model):
    #id = models.AutoField(primary_key=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, blank=False, null=False)
    start_date = models.DateField(default=date.today, blank=False, null=False)
    completed = models.BooleanField(default=False ,null=False)
    title = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    class Meta:
        ordering = ['completed','start_date', 'id']