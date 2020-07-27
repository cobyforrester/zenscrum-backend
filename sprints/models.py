from datetime import date
from django.db import models
from projects.models import Project

class Sprint(models.Model):
    #id = models.AutoField(primary_key=True)
    #Need to make sure project_sprint is NOT NULL
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=False, null = False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    goal = models.TextField(blank=False, null=False)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    class Meta:
        ordering = ['id']