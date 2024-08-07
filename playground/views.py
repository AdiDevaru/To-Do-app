from django.shortcuts import render, redirect #type: ignore

from django.views.generic.list import ListView #type: ignore
from django.views.generic.detail import DetailView #type: ignore
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView #type: ignore
from django.urls import reverse_lazy #type: ignore

from django.contrib.auth.views import LoginView #type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore
from django.contrib.auth import login #type: ignore


from .models import Task

#User Authentication
class CustomLoginView(LoginView):
    template_name = 'playground/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterUser(FormView):
    form_class = UserCreationForm
    #redirect_authenticated_user = True
    template_name = 'playground/register.html'
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterUser, self).get(*args, **kwargs)
    

#CRUD Operations
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks' #context dict
    
    def get_context_data(self, **kwargs):
        #getting user specific data
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        #search
        search = self.request.GET.get('search_item') or ''
        if search:
            context['tasks'] = context['tasks'].filter(title__startswith=search)
        context['search'] = search
        
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'playground/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateView, self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'playground/task_delete.html'
    