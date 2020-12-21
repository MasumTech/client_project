from django.contrib import admin
from .models import Project,Categorey,Job,JobDepartment,JobApplication
# Register your models here.
admin.site.register(Project)
admin.site.register(Categorey)
admin.site.register(Job)
admin.site.register(JobDepartment)
admin.site.register(JobApplication)