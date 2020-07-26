from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.conf import settings #for safe redirect, users
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url #for safe redirect
from django.contrib.auth.models import User


from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Project, UserProject
from .forms import ProjectForm
from .serializers import ProjectSerializerPost, ProjectSerializerGet, ProjectActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

from .models import Project

def projects_home_view(request, *args, **kwargs):
    return render(request, 'projects/projects.html', context={}, status=200)

#using django rest framework, wayyy cleaner
#this posts data to projects
@api_view(['POST'])
#@authentication_classes([SessionAuthentication, CustomAuthentication])
@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
def project_create_view(request, *args, **kwargs):
    print(request.POST)
    if request.POST:
        serializer = ProjectSerializerPost(data=request.POST)
    else:
        serializer = ProjectSerializerPost(data=request.data)
    if serializer.is_valid(raise_exception=True):
        
        serializer.save(user=request.user)
        obj = Project.objects.get(id=serializer.data['id'])
        new_serializer = ProjectSerializerGet(obj) #gets all attributes of new object
        return Response(new_serializer.data, status=201)
    return Response({}, status=400)

#gets projects
# and *** means it was commented for react, beginning correct after should be removed
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_projects(request, *args, **kwargs):
    all_project_ids = calc_ids(request.user.username)
    #now sort project ids and create queryset
    all_project_ids.sort(reverse=True)
    qs = Project.objects.filter(id__in=all_project_ids)
    serializer = ProjectSerializerGet(qs, many=True)
    #serializer = ProjectSerializerGet(Project.objects.all(), many=True) # *** for testing react
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_details(request, project_id, *args, **kwargs):
    qs = Project.objects.filter(id=project_id)
    valid_projects = calc_ids(request.user.username)
    if not qs.exists():
        return Response({}, status=404)
    elif project_id not in valid_projects:
        return Response({}, status=403)
    obj = qs.first()
    serializer = ProjectSerializerGet(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id, *args, **kwargs):
    qs = Project.objects.filter(id=project_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({'message': 'You cannot delete this Project'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Project removed'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def project_action_member(request, *args, **kwargs):
    '''
    id is required
    member username is required
    Action options are for member: add, remove
    '''
    serializer = ProjectActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        project_id = data.get('id')
        action = data.get('action')
        members_username = data.get('member')

    #users cannot add or remove themselves 
    if request.user.username == members_username :
        return Response({'message': 'Cannot add or remove yourself'}, status=404)
    qs = Project.objects.filter(id=project_id)
    if not qs.exists():
        return Response({'message': 'Project not found'}, status=404)
    qs = qs.filter(user=request.user)
    obj = qs.first()
    #if no object exists then they do not have access
    if not obj:
        return Response({'message': 'You do not have ownerhip of this project'}, status=403)
    #for if the user is not found
    try:
        member = User.objects.get(username=members_username)
    except:
        return Response({'message': 'User does not exist'}, status=404)
    if action == 'add' and obj and not obj.members.filter(username=members_username):
        obj.members.add(member)
        serializer = ProjectSerializerGet(obj)
        return Response(serializer.data, status=200)
    elif action == 'remove' and obj and obj.members.filter(username=members_username):
        obj.members.remove(member)
        serializer = ProjectSerializerGet(obj)
        return Response(serializer.data, status=200)
    elif action == 'view':
        pass #this is to do
    return Response({'message': 'No action, user either already added or removed'}, status=400)

# ============================== Helper Functions ===================================
def calc_ids(username): 
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


# ================================== PURE DJANGO BELOW (not in use) ================================
def project_create_view_pure_django(request, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    #This is for checking the user is valid
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax:
            return JsonResponse({}, status = 401) #not authorized
        return redirect(settings.LOGIN_URL)
    #We are processing the form here for a POST and getting the next url desired
    form = ProjectForm(request.POST or None)
    next_url = request.POST.get('next') or None
    #form is valid, save and if ajax JsonResponse else redirect to next_url
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user #adding user to object
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        #should be a safe url!
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = ProjectForm()
    #if errors and ajax return errors
    if form.errors and request.is_ajax():
        return JsonResponse(form.errors, status=400)
    #finally return if not ajax and errors
    return render(request, 'components/form.html', context={'form': form})

def project_details_pure_django(request, project_number, *args, **kwargs):
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
        data['user'] = obj.user
        data['progress'] = obj.progress
        data['description']: obj.description
        status = 200
    except:
        data['message'] = 'Not Found'
        status = 404
    return JsonResponse(data, status=status)

def print_all_projects_pure_django(request, *args, **kwargs):
    '''
    REST API VIEW
    Consume by JavaScript/React
    return Json
    '''
    qs = Project.objects.all()
    sprint_list = [x.serialize() for x in qs]
    data = {
        'response': sprint_list
    }
    return JsonResponse(data)