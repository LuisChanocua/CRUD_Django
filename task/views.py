from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from django.shortcuts import get_object_or_404


# Se importa el modelo de las tareas con un nombre
# para no confundir con la view
from .models import tasks as TaskModel


# Create your views here.
def singup(request):

    # manda el formulario a la vista
    if request.method == 'GET':

        return render(request, 'singup.html', {
            'form': UserCreationForm
        })
    else:
        # registra el usuario en la db cuando manda el form con POST
        if request.POST['password1'] == request.POST['password2'] and request.POST['username'] != "":

            try:

                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    "error": 'Ya existe el usuario',

                })
        else:

            return render(request, 'singup.html', {
                'form': UserCreationForm,
                "error": 'Passwords no coinciden',

            })


def home(request):
    return render(request, 'home.html')

# Views para las tareas


def tasks(request):
    task = TaskModel.objects.filter(user=request.user, datecompleted__isnull = True)
    
    
    return render(request, 'tasks.html',{'tasks': task})


def createtask(request):
    if request.method == 'GET':
        return render(request, 'createtask.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'createtask.html',{
                'form': TaskForm,
                'error': 'Error to try save the task, complete all inputs'
            })
        
def task_detail(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    
    return render(request, 'task_detail.html',{'task': task})

# Views para las sing in and out
def singout(request):
    logout(request)
    return redirect('home')


def singin(request):
    form = AuthenticationForm(request, data=request.POST)
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': form
        })
    else:
        if form.is_valid():

            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])

            if user is None:
                return render(request, 'singin.html', {
                    'form': form,
                    "error": 'Password or username incorrect'
                })
            else:
                login(request, user)
                return redirect('tasks')
        else:
            return render(request, 'singin.html', {
                'form': form,
                "error": "Complete the inputs"
            })
