from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.conf import settings #for safe redirect, users
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url #for safe redirect

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Project, UserProject
from .forms import ProjectForm
from .serializers import ProjectSerializer

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
    serializer = ProjectSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(puser=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

#gets projects
@api_view(['GET'])
def view_projects(request, *args, **kwargs):
    qs = Project.objects.all()
    serializer = ProjectSerializer(qs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def project_details(request, project_id, *args, **kwargs):
    qs = Project.objects.filter(id=project_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = ProjectSerializer(obj)
    return Response(serializer.data, status=200)

@permission_classes([IsAuthenticated]) #if user is authenticated can do otherwise no
@api_view(['DELETE', 'POST'])
def delete_project(request, project_id, *args, **kwargs):
    qs = Project.objects.filter(id=project_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(puser=request.user)
    if not qs.exists():
        return Response({'message': 'You cannot delete this Project'}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Project removed'}, status=200)



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
        obj.puser = user #adding user to object
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
        data['owner'] = obj.owner
        data['progress'] = obj.owner
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