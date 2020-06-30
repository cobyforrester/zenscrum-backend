from django.db import models

class Sprint(models.Model):
    #id = models.AutoField(primary_key=True)
    number = models.SmallIntegerField(default=-1, blank=False, null=False)
    date = models.TextField(default='AddDate', blank=False, null=False)
    goal = models.TextField(default='AddGoal', blank=False, null=False)
    image = models.FileField(upload_to='images/', blank=True, null=True)
