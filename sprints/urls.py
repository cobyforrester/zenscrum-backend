from django.urls import path

from sprints.views import (
    sprint_create_view,
    view_sprints,
    delete_sprint,
    sprint_details
)
'''
CLIENT
Base ENDPOINT  /api/projects/
'''
urlpatterns = [
    #sprints
    path('<int:project_id>/', view_sprints),
    path('create/', sprint_create_view),
    path('<int:sprint_id>/delete/', delete_sprint),
    path('<int:sprint_id>/details/', sprint_details),
]
