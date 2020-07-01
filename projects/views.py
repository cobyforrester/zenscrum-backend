from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Project
def projects_home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)