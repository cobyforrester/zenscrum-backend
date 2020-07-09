from django.contrib import admin

# Register your models here.
from .models import Project, UserProject

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'puser'] #this just displays for the admin the values
    search_fields = ['title','puser__username', 'puser__email']

    class Meta:
        model = Project
    
    #if i want to display admin easier
    #def __str__(self):
    #    return self.title

admin.site.register(Project, ProjectAdmin)
#admin.site.register(UserProject)