from django.urls import path

from sprints.views import (
    sprint_create_view
)
'''
CLIENT
Base ENDPOINT  /api/projects/
'''
urlpatterns = [
    #sprints
    path('create/', sprint_create_view),
]
