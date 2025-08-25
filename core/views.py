from django.shortcuts import render,redirect
from rest_framework import response ,viewsets,status
from rest_framework.permissions import IsAuthenticated
from .models import Task,Room,Topics
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
    context = {'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'home.html',context)

def room (request,pk):
    room = Room.objects.get(id=pk)
    return render(request,'room.html',{'room':room})

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'delete.html')

class TaskViewSet(viewsets.ModelViewSet):
    task = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.all()
    