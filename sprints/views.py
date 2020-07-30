from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import SprintSerializerPost, SprintSerializerGet

from projects.models import UserProject, Project
from .models import Sprint
def sprints_home_view(request, project_number, *args, **kwargs):
    #do something with project number
    return render(request, 'sprints/sprints.html', context={}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def sprint_create(request, *args, **kwargs):
    print('here')
    serializer = SprintSerializerPost(data=request.data)
    # CHECK IF USER HAS AUTHORITY TO CREATE SPRINT
    project_obj = Project.objects.get(id=request.data['project'])
    if request.user.username != project_obj.user.username:
        return Response({}, status=401)
    if serializer.is_valid(raise_exception=True):
        serializer.validated_data
        serializer.save()
        obj = Sprint.objects.get(id=serializer.data['id'])
        new_serializer = SprintSerializerGet(obj) #gets all attributes of new object
        return Response(new_serializer.data, status=201)
    return Response({}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def sprint_update(request, sprint_id, *args, **kwargs):
    sprint_obj = Sprint.objects.get(id=sprint_id)
    if request.user.username != sprint_obj.project.user.username:
        return Response({}, status=401)
    try:
        # SHOULD VALIDATE DATA
        obj = Sprint.objects.get(id=sprint_id)
        obj.goal = request.data['goal']
        obj.start_date = request.data['start_date']
        obj.end_date = request.data['end_date']
        obj.save()
    except:
        return Response({}, status=400)
    new_serializer = SprintSerializerGet(obj) #gets all attributes of new object
    return Response(new_serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_sprints(request, project_id, *args, **kwargs): 
    all_project_ids = calc_project_ids(request.user.username)
    #now sort project ids and create queryset
    if project_id in all_project_ids:
        qs = Sprint.objects.filter(project=project_id) #we want project id to query all sprints
        serializer = SprintSerializerGet(qs, many=True)
        return Response(serializer.data, status=200)
    return Response({'message': 'You cannot access these sprints'}, status=401)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_sprint(request, sprint_id, *args, **kwargs):
    qs = Sprint.objects.filter(id=sprint_id)
    if not qs.exists():
        return Response({'message': 'Sprint not found'}, status=404)
    qs = qs.filter(project__user__username=request.user.username)
    if not qs.exists():
        return Response({'message': 'You cannot delete this sprint'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Sprint removed'}, status=200)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def sprint_details(request, sprint_id, *args, **kwargs):
    qs = Sprint.objects.filter(id=sprint_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    print(obj.project.members)

    #for seeing if they have access to project
    found = False
    qs = UserProject.objects.all()
    for i in qs:
        if i.project.id == obj.project.id and i.user.username == request.user.username:
            found = True
    if obj.project.user.username == request.user.username or found:
        serializer = SprintSerializerGet(obj)
        return Response(serializer.data, status=200)
    return Response({}, status=401) 


# ============================= HELPER FUNCTIONS =============================

def calc_project_ids(username): 
    '''
    This calculates the project id's our user is a part of
    '''
    all_project_ids = []
    qs = UserProject.objects.all()
    for i in qs:
        if i.user.username == username and i.project.id not in all_project_ids:
            all_project_ids.append(i.project.id)
    #for all projects user is a member of 
    qs = Project.objects.all()
    for i in qs:
        if i.user.username == username and i.id not in all_project_ids:
            all_project_ids.append(i.id)
    return all_project_ids




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

def django_sprint_details(request, sprint_number, *args, **kwargs):
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