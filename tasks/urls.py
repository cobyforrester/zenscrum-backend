from django.urls import path

from tasks.views import (
    task_create,
    view_tasks,
    delete_task,
    task_details,
    task_update,
)
'''
CLIENT
Base ENDPOINT  /api/tasks/
'''
urlpatterns = [
    #tasks
    path('<int:sprint_id>/', view_tasks),
    path('create/', task_create),
    path('<int:task_id>/delete/', delete_task),
    path('<int:task_id>/details/', task_details),
    path('<int:task_id>/update/', task_update),
]
