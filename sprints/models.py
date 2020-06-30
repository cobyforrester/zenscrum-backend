from datetime import date
from django.db import models

class Sprint(models.Model):
    #id = models.AutoField(primary_key=True)
    project_id = models.IntegerField(default=-1, blank=False, null=False)
    number = models.SmallIntegerField(default=-1, blank=False, null=False)
    date = models.DateField(default=date.today, blank=False, null=False)
    goal = models.TextField(default='AddGoal', blank=False, null=False)
    image = models.FileField(upload_to='images/', blank=True, null=True)
