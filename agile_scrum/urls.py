"""agile_scrum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView



from sprints.views import sprints_home_view, sprint_details, sprint_list_view
from projects.views import (
    projects_home_view, 
    project_details, 
    view_projects, 
    project_create_view, 
    delete_project, 
    project_action_member
)
urlpatterns = [
    path('admin/', admin.site.urls),

    #test
    path('react/', TemplateView.as_view(template_name='react.html')),

    #sprints
    path('sprints-home/<int:project_number>', sprints_home_view),
    path('sprints/<int:project_id>', sprint_list_view),
    path('sprint/<int:sprint_number>', sprint_details),

    #projects
    path('', projects_home_view),
    path('create-project', project_create_view),
    path('view-projects', view_projects),
    path('project/<int:project_id>', project_details),
    #path('api/projects/<int:project_id>/delete', delete_project),
    #path('api/projects/action', project_action_member),

    path('api/projects/', include('projects.urls')),
    path('api/auth/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)