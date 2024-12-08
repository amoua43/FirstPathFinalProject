from django.forms import ModelForm
from .models import Room, Project
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # ['name', 'body']
        exclude = ['host', 'participants']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link']

from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'time', 'major']

# added for job search implementation
class JobSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False, label="Job Title")
    location = forms.CharField(max_length=100, required=False, label="Location")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'title' in self.data:
            self.fields['title'].initial = self.data['title']
        
        if 'location' in self.data:
            self.fields['location'].initial = self.data['location']
