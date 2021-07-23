from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Todo
from .forms import TodoForm
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger('django')


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



# Create your views here.

def index(request):
    todo_list = Todo.objects.order_by('id')
    form = TodoForm()

    context = {'todo_list': todo_list,
               'form':form}
    
    return render(request,'todo/index.html',context)

@require_POST
def addTodo(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        new_todo = form.save()
        logger.info('New Todo added')
    return redirect('todo-index')  

def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()
    logger.info('Todo Completed')
    return redirect('todo-index')

def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True).delete()
    logger.info('Todo Delete Completed')
    return redirect('todo-index')
    

def deleteAll(request):
    Todo.objects.all().delete()
    logger.info('Todo Deleted All')
    return redirect('todo-index')
