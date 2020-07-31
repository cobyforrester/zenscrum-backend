from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializerPost, TaskSerializerGet

from projects.models import UserProject, Project
from sprints.models import Sprint
from .models import Task


@api_view(['POST'])
@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def task_create(request, *args, **kwargs):

    all_project_ids = calc_project_ids(request.user.username)
    #now sort project ids and create queryset
    project_id = Sprint.objects.get(id=request.data['sprint']).project.id
    if project_id not in all_project_ids:
        return Response({}, 401)

    serializer = TaskSerializerPost(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.validated_data
        serializer.save()
        obj = Task.objects.get(id=serializer.data['id'])
        new_serializer = TaskSerializerGet(obj) #gets all attributes of new object
        return Response(new_serializer.data, status=201)
    return Response({}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def task_update(request, task_id, *args, **kwargs):
    try:
        # VALIDATE USER
        all_project_ids = calc_project_ids(request.user.username)
        sprint_id = Task.objects.get(id=task_id).sprint.id
        project_id = Sprint.objects.get(id=sprint_id).project.id
        if project_id not in all_project_ids:
            return Response({}, 401)
        
        obj = Task.objects.get(id=task_id)
        obj.title = request.data['title']
        obj.description = request.data['description']
        obj.completed = request.data['completed']
        obj.save()
    except:
        return Response({}, status=400)
    new_serializer = TaskSerializerGet(obj) #gets all attributes of new object
    return Response(new_serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_tasks(request, sprint_id, *args, **kwargs):
    try:
        all_project_ids = calc_project_ids(request.user.username)
        project_id = Sprint.objects.get(id=sprint_id).project.id
        if project_id not in all_project_ids:
            return Response({}, 401)
        #now sort project ids and create queryset
        qs = Task.objects.filter(sprint=sprint_id) #we want project id to query all sprints
        serializer = TaskSerializerGet(qs, many=True)
    except:
        return Response({}, status=404)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id, *args, **kwargs):
    try:
        # VALIDATE USER
        all_project_ids = calc_project_ids(request.user.username)
        sprint_id = Task.objects.get(id=task_id).sprint.id
        project_id = Sprint.objects.get(id=sprint_id).project.id
        if project_id not in all_project_ids:
            return Response({}, 401)
        
        obj = Task.objects.get(id=task_id)
        obj.delete()
    except:
        return Response({}, status=404)
    return Response({'message': 'Task removed'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_details(request, task_id, *args, **kwargs):
    try:
        # VALIDATE USER
        all_project_ids = calc_project_ids(request.user.username)
        sprint_id = Task.objects.get(id=task_id).sprint.id
        project_id = Sprint.objects.get(id=sprint_id).project.id
        if project_id not in all_project_ids:
            return Response({}, 401)

        obj = Sprint.objects.get(id=task_id)
        serializer = TaskSerializerGet(obj)
    except:
        return Response({}, status=404)
    return Response(serializer.data, status=200)
    


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