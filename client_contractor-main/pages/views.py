from contractor.settings import EMAIL_HOST, EMAIL_HOST_USER
from pages.models import Project,Categorey,Job,JobApplication
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.core.mail import EmailMessage
# Create your views here.
from .forms import ApplicationForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def home(request):
    home_list = Project.objects.order_by('-pub_date')[:4]
    context = {
        'home_list': home_list,
    }
    return render(request, 'pages/home.html',context)

def projects(request):
    project_list = Project.objects.all()
    category_list = Categorey.objects.all()
    context ={
        'project_list': project_list,
        'category_list': category_list,
    }
    return render(request, 'pages/projects.html',context)


# def category_filter(request):
#     category_filter_list = Project.objects.all()
#
#     context ={
#
#     }
#     return render(request, 'pages/projects.html',context)


def projects_details(request,slug):
    project = Project.objects.filter(slug=slug)
    
    if project.exists():
        project = project.first()
    else:
        HttpResponse("<h3>page not found</h3>")
    
    context = {
        'project': project,
        
    }

    return render(request, 'pages/projects_details.html',context)


# def contact(request):
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         email = request.POST['email']
#         send_mail(subject,message,email,['contact@fieldviewcontractors.com'],fail_silently=False)
#     return render(request, 'pages/contact.html')

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ApplicationForm, ContactForm



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name   = form.cleaned_data['name']
            email_from =  form.cleaned_data['email_from']   
            email_to = EMAIL_HOST_USER   
            message= form.cleaned_data['message']
            #send_mail(subject, message, email_from, [email_to,], fail_silently=False)
            email = EmailMessage(subject=subject,body=message,from_email=email_from,to=[email_to,],reply_to=[email_from],)
            email.send()
            return render(request, 'pages/contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def careers(request):
    jobs = Job.objects.all().order_by('-pub_date')
    context ={
        'jobs': jobs,
    }
    return render(request, "pages/careers.html",context)


# def job_details(request,slug):
#     jobs = Job.objects.filter(slug=slug)

#     context ={
#         'jobs': jobs,
#     }
#     return render(request, 'pages/job_details.html',context)

# def job_details(request,slug):
#     jobs = Job.objects.filter(slug=slug)
#     form = ApplicationForm()
#     if request.method == 'POST':
#         form = ApplicationForm(request.POST)
#         if form.is_valid():
#             #cementry is a variable
#             cemetery=form.save(commit=False)
#             cemetery.applied_position=request.POST.get('applied_position')
#             cemetery.resume=request.POST.get('resume')  
#             cemetery.first_name = request.POST.get('first_name')
#             cemetery.last_name=request.POST.get('last_name')
#             cemetery.email=request.POST.get('email')
#             cemetery.street_address=request.POST.get('street_address')
#             cemetery.city=request.POST.get('city')
#             cemetery.state=request.POST.get('state')
#             cemetery.zip_code=request.POST.get('zip_code')
#             cemetery.phone=request.POST.get('phone')
#             cemetery.save() 
#             print('submitted...........')
#             return render(request, 'pages/job_details.html',{'form': form,})
  
#     else:
#         form = ApplicationForm()
#     context ={
#         'jobs': jobs,
#         'form': form,
#     }
#     return render(request, 'pages/job_details.html',context)
    
#job application form

def job_details(request,slug):
    jobs = Job.objects.filter(slug=slug)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            #cementry is a variable
            
            applied_position=request.POST.get('applied_position','')
            resume=request.FILES['resume']
            first_name = request.POST.get('first_name','')
            last_name=request.POST.get('last_name','')
            email=request.POST.get('email','')
            street_address=request.POST.get('street_address','')
            city=request.POST.get('city','')
            state=request.POST.get('state','')
            zip_code=request.POST.get('zip_code','')
            phone=request.POST.get('phone','')
            cs = JobApplication(applied_position=applied_position,resume=resume,first_name =first_name,last_name=last_name,email=email,street_address=street_address,city=city,state=state,zip_code=zip_code,phone=phone)
            cs.save()
            print('submitted...........')
            return render(request, 'pages/job_details.html',{'form': form,})
  
    else:
        form = ApplicationForm()
    context ={
        'jobs': jobs,
        'form': form,
    }
    return render(request, 'pages/job_details.html',context)