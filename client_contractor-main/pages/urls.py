from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name = 'home'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>', views.projects_details, name ='project'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name ='careers'),
    #path('job_details/', views.job_details, name ='job_details'),
    path('jobs/<slug:slug>', views.job_details, name = 'jobs'),


]
