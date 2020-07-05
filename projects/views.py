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
        data['begin_date'] = obj.begin_date
        data['title'] = obj.title
        data['project_id'] = obj.id
        data['owner'] = obj.owner
        data['progress'] = obj.owner
        data['description']: obj.description
        status = 200
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)

def print_all_projects(request, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    qs = Project.objects.all()
    sprint_list = [{'begin_date': x.begin_date, 'title': x.title, 'description': x.description, 'id': x.id, 'owner': x.owner, 'progress': x.progress} for x in qs]
    data = {
        'response': sprint_list
    }
    return JsonResponse(data)