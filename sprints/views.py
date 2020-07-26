from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import SprintSerializerPost, SprintSerializerGet

from .models import Sprint
def sprints_home_view(request, project_number, *args, **kwargs):
    #do something with project number
    return render(request, 'sprints/sprints.html', context={}, status=200)


@api_view(['POST'])
#@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def sprint_create_view(request, *args, **kwargs):
    if request and request.POST:
        serializer = SprintSerializerPost(data=request.POST)
    elif request and request.data:
        serializer = SprintSerializerPost(data=request.data)
    else:
        return Response({}, status=400)
    # CHECK IF USER HAS AUTHORITY TO CREATE SPRINT
    if serializer.is_valid(raise_exception=True):
        serializer.validated_data
        sprint_number = calc_sprint_num(serializer.validated_data['project'])
        serializer.save(number=sprint_number)
        #print(Sprint.objects.all().first().number)
        obj = Sprint.objects.get(id=serializer.data['id'])
        print(obj)
        new_serializer = SprintSerializerGet(obj) #gets all attributes of new object
        return Response(new_serializer.data, status=201)
    return Response({}, status=400)

def calc_sprint_num(project_id):
    return Sprint.objects.filter(project=project_id).count() + 1




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