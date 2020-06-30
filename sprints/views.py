from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from .models import Sprint
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

def sprint_details(request, sprint_number, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    data = {
        'sprint_number': sprint_number,
        #'image': obj.image.url
    }
    try:
        obj = Sprint.objects.get(number=sprint_number)
        data['date'] = obj.date
        data['goal'] = obj.goal
        status = 200
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)