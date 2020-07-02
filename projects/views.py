from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Project
def projects_home_view(request, *args, **kwargs):
    return render(request, 'projects/projects.html', context={}, status=200)

def project_details(request, project_number, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    data = {
        #'image': obj.image.url
}
    try:
        obj = Project.objects.get(id=project_number)
        data['date'] = obj.date
        data['goal'] = obj.goal
        data['number'] = obj.number
        data['project_id'] = obj.sprint_project.id
        status = 200
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)