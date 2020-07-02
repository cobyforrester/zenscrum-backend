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
from django.contrib import admin
from django.urls import path

from sprints.views import sprints_home_view, sprint_details, sprint_list_view
from projects.views import projects_home_view, project_details
urlpatterns = [
    path('admin/', admin.site.urls),

    #sprints
    path('sprints_home/<int:project_number>', sprints_home_view),
    path('sprints', sprint_list_view),
    path('sprint/<int:sprint_number>', sprint_details),

    #projects
    path('', projects_home_view),
    path('projects/<int:project_number>', project_details),
]
