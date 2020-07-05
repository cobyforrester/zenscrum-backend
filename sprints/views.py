from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Sprint
def sprints_home_view(request, project_number, *args, **kwargs):
    #do something with project number
    return render(request, 'sprints/sprints.html', context={}, status=200)

def sprint_list_view(request, project_id, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    qs = Sprint.objects.all()
    sprint_list = []
    for x in qs:
        if x.project_sprint.id == project_id:
            tmp = {
                'start_date': x.start_date, 
                'goal': x.goal, 
                'project_id': x.project_sprint.id, 
                'number': x.number
            }
            sprint_list.append(tmp)
    data = {
        'response': sprint_list
    }
    return JsonResponse(data)

def sprint_details(request, sprint_number, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    data = {
        #'image': obj.image.url
}
    try:
        obj = Sprint.objects.get(number=sprint_number)
        data['start_date'] = obj.start_date
        data['goal'] = obj.goal
        data['number'] = obj.number
        data['project_id'] = obj.project.id
        status = 200
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)