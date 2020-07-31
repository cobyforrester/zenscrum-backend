from django.urls import path

from sprints.views import (
    sprint_create,
    view_sprints,
    delete_sprint,
    sprint_details,
    sprint_update,
)
'''
CLIENT
Base ENDPOINT  /api/sprints/
'''
urlpatterns = [
    #sprints
    path('<int:project_id>/', view_sprints),
    path('create/', sprint_create),
    path('<int:sprint_id>/delete/', delete_sprint),
    path('<int:sprint_id>/details/', sprint_details),
    path('<int:sprint_id>/update/', sprint_update),
]
