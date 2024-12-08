from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message, Project, Event, Job
from .forms import RoomForm, ProjectForm, EventForm, JobSearchForm





# rooms = [
#     {'id':1, 'name' : 'Job Posting page!'},
#     {'id':2, 'name' : 'Profile settings '},
#     {'id':3, 'name' : 'Feature 1'},
# ]


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = user.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist!')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password Does not exist')
    context = {'page' : page}
    return render(request, 'base/login_registration.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_registration.html', {'form': form})

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #search function to seach using keywords
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count() #use for total no. of jobs
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)






def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context = {'room' : room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_messages' : room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='/login') #can create a job posting only if they are auth user
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)




@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('<h3>You do not have the access to update this job details!<h3>')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)




@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('<h3>You do not have the access to delete this job details!<h3>')

    if request.method == 'POST' :
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})




@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('<h3>Not allowed!<h3>')

    if request.method == 'POST' :
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


#job description & job related stuff
#def jobDetails(request):
#    return render(request)





def project_list(request):
    projects = Project.objects.all().order_by('-created')
    context = {'projects': projects}
    return render(request, 'base/project_list.html', context)

@login_required(login_url='/login/')
def add_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project-list')
    context = {'form': form}
    return render(request, 'base/add_project.html', context)





@login_required(login_url='login')
def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            return redirect('events-list')  # Redirect to the events list
    context = {'form': form}
    return render(request, 'base/create_event.html', context)


def events_list(request):
    events = Event.objects.all().order_by('date', 'time')  # Order by date and time
    q = request.GET.get('q') if request.GET.get('q') else ''
    if q:
        events = events.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(major__icontains=q)
        )
    context = {'events': events}
    return render(request, 'base/events_list.html', context)


###added for Job serach functionality

def job_search(request):

    jobs = Job.objects.all()  # Default :  retrieve all jobs
    form = JobSearchForm(request.POST or None) 
    #jobs = None
    #checking if data satisfies the search criteria
    if request.method == 'POST' and form.is_valid():
        #Filter jobs based on search criteria

        title = form.cleaned_data.get('title')  
        location = form.cleaned_data.get('location')
        
        #filtering by title
        if title:
            jobs = jobs.filter(jobtitle__icontains=title) #case-insenitive title search

        #filtering by location 
        if location:
            jobs = jobs.filter(location__icontains = location) #case-insensitive location search  complocation

    return render(request, 'base/job_search.html', {'form': form, 'jobs': jobs})

def job_description(request,pk):
    #retrieve job object by id (pk) from database
    job1 = Job.objects.get(id=pk)
    #creating a dictionary to store the job object as context for the template
    context = {'job1': job1}
    #render the job description HTML template with the job object as context
    return render(request,'base/job_description.html', context)




def layout(request):
    return render(request, 'base/layout.html')
def about_us(request):
    return render(request, 'base/about_us.html')
def contact_us(request):
    return render(request, 'base/contact_us.html')
# def projects_landing(request):
#     return render(request, 'base/projects.html')
def events(request):
     return render(request, 'base/events.html') 
def sign_up(request):
     return render(request, 'base/sign_up.html')
#def loginPage(request):
#    return render(request, 'base/login.html')
def landing_page(request):
    return render(request, 'base/landing_page.html')








