from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.conf import settings #for safe redirect
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url #for safe redirect

from .models import Project, UserProject
from .forms import ProjectForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

from .models import Project
def projects_home_view(request, *args, **kwargs):
    return render(request, 'projects/projects.html', context={}, status=200)

def project_create_view(request, *args, **kwargs):
    form = ProjectForm(request.POST or None)
    next_url = request.POST.get('next') or None

    if form.is_valid():
        obj = form.save(commit=False)
        #form related logic here
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        #should be a safe url!
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = ProjectForm()
    if form.errors and request.is_ajax():
        return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={'form': form})

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
    sprint_list = [x.serialize() for x in qs]
    data = {
        'response': sprint_list
    }
    return JsonResponse(data)