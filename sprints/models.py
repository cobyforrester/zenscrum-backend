from datetime import date
from django.db import models
from projects.models import Project

class Sprint(models.Model):
    #id = models.AutoField(primary_key=True)
    #Need to make sure project_sprint is NOT NULL
    project_sprint = models.ForeignKey(Project, on_delete=models.CASCADE, null =True)
    number = models.SmallIntegerField(default=-1, blank=False, null=False)
    start_date = models.DateField(default=date.today, blank=False, null=False)
    end_date = models.DateField(default=date.today, blank=False, null=False)
    goal = models.TextField(default='AddGoal', blank=False, null=False)
    image = models.FileField(upload_to='images/', blank=True, null=True)
