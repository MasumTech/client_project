from django.db import models
import datetime
from django.forms import forms
from django.forms.fields import FileField
from django.urls import reverse
from django.db import models
# slug
from django.utils.text import slugify
from random import random
from django.db.models.signals import pre_save
# Create your models here.

def year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def current_year():
    return datetime.date.today().year


class Categorey(models.Model):
    title = models.CharField(max_length=70)

    def __str__(self):
        return self.title
        
class Project(models.Model):
    title = models.CharField(max_length=55)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    description = models.TextField()
    min_budget = models.IntegerField(blank=True, null=True)
    max_budget = models.IntegerField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    services = models.CharField(max_length=55)
    image1 = models.ImageField(upload_to='photos/%Y/%m/%d')
    image2 = models.ImageField(upload_to='photos/%Y/%m/%d')
    categories = models.ManyToManyField(Categorey)
    location = models.CharField(max_length=140, blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(('year'), choices=year_choices(), default=current_year, blank=True, null=True)
    is_published = models.BooleanField(default=True)

    
    def __str__(self):
        return self.title
        


    def get_absolute_url(self):
        return reverse('project',kwargs={ 'slug': self.slug})

def create_slugy(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Project.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slugy(instance, new_slug=new_slug)
    return slug
    
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slugy(instance)
pre_save.connect(pre_save_receiver, Project)


# for job purpose work

class JobDepartment(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Job(models.Model):
    
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    department = models.ForeignKey(JobDepartment, on_delete=models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(max_length=2000)
    requirements = models.TextField(max_length=2200)
    responsibilities = models.TextField(max_length=2200)
    #applications_received = models.ManyToManyField(JobApplication, blank=True, default=None)
    pub_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return self.title
        


    def get_absolute_url(self):
        return reverse('jobs',kwargs={ 'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Job.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_receiver, Job)


class JobApplication(models.Model):
    applied_position = models.CharField(max_length=160, blank=True, null=True)
    resume = models.FileField(upload_to='files', null=True)
    #resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    first_name = models.CharField(max_length=60, blank=True, null=True)
    last_name = models.CharField(max_length=60, blank=True, null=True)
    email = models.EmailField(max_length=60, blank=True, null=True)
    
    #job_position = models.ManyToManyField('Job', blank=True, default=None)
    street_address = models.CharField(max_length=140, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=60, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    applied_date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.first_name