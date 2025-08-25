from django.urls import path,include
from .views import TaskViewSet,home,room,createRoom,updateRoom,deleteRoom
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'task',TaskViewSet,basename='task')

urlpatterns = [
    # path('',include(router.urls)),
    path('',home,name='home'),
    path('room/<int:pk>/',room,name = 'room'),
    path('create-room',createRoom, name = 'create-room'),
    path('update-room/<str:pk>',updateRoom,name ='update-room'),
    path('delete-room/<str:pk>',deleteRoom,name ='delete-room')

]
