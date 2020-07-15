from django.urls import path

from projects.views import (
    projects_home_view, 
    project_details, 
    view_projects, 
    project_create_view, 
    delete_project, 
    project_action_member
)
'''
CLIENT
Base ENDPOINT  /api/projects/
'''
urlpatterns = [
    #projects
    path('', view_projects),
    path('action/', project_action_member),
    path('create/', project_create_view),
    path('<int:project_id>/', project_details),
    path('<int:project_id>/delete/', delete_project),
]
