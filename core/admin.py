from django.contrib import admin
from .models import Task,Message,Topics,Room
# Register your models here.
admin.site.register(Task)
admin.site.register(Message)
admin.site.register(Topics)
admin.site.register(Room)