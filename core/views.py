from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from rest_framework import response ,viewsets,status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Task,Room,Topics,Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .serializers import TaskSerializer
from .forms import RoomForm
from django.db.models import Q
# Create your views here.

def home(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q )|
        Q(descriptions__icontains=q) ) 
    topics = Topics.objects.all()
    room_count = rooms.count()
    recent_activity = Message.objects.filter(Q(room__topic__name__icontains =q ))
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'recent_activity':recent_activity}
    return render(request,'home.html',context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')                
        try:
            user = User.objects.get(username=username)            
        except:
            messages.error(request,'User does not exist')
        
        user =authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or Password in invalid..')
    context ={'page':page}     
    return render(request,'loginRegister.html',context)

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error as occured')   
    return render(request,'loginRegister.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('home')

def room (request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
    return render(request,'room.html',{'room':room,'room_messages':room_messages,'participants':participants})

@login_required
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Your are not allowed to do this..")
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'room_form.html',context)

@login_required
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed to do this..")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html')

@login_required
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        HttpResponse('You are not allowed to it')
        
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'delete.html',{'obj':message})

class TaskViewSet(viewsets.ModelViewSet):
    task = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.all()
    