from django.contrib import admin #type: ignore
from .models import Task

admin.site.register(Task)
