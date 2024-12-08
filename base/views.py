from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id':1, 'name' : 'Job Posting page!'},
#     {'id':2, 'name' : 'Profile settings '},
#     {'id':3, 'name' : 'Feature 1'},
# ]


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
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
    context = {}
    return render(request, 'base/login_registration.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

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

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room' : room}
    return render(request, 'base/room.html', context)


@login_required(login_url='/login') #can create a job posting only if they are auth user
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
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

def layout(request):
    return render(request, 'base/layout.html')
def about_us(request):
    return render(request, 'base/about_us.html')
def contact_us(request):
    return render(request, 'base/contact_us.html')
def projects(request):
    return render(request, 'base/projects.html')
def events(request):
    return render(request, 'base/events.html') 
def sign_up(request):
    return render(request, 'base/sign_up.html')
def loginPage(request):
    return render(request, 'base/login.html')
def landing_page(request):
    return render(request, 'base/landing_page.html')
