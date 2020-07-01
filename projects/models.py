from datetime import date
from django.db import models

class Project(models.Model):
    title = models.TextField(default='AddTitle', blank=False, null=False)
    begin_date = models.DateField(default=date.today, blank=False, null=False)
    description = models.TextField(default='AddGoal', blank=False, null=False)
