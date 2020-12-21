from pages.models import Job, JobApplication
from django import forms
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    #phone = forms.CharField(required=True)
    email_from = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        #fields ='__all__'
        fields=('applied_position','resume','first_name','last_name','email','street_address','city','state','zip_code','phone',)