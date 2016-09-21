from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo
from django.urls import reverse
from .controllers import getAllCourses

# Create your views here.
def index(request):
    #save username
    username = request.POST.get('username', 'olawo')    

    #prep todos
    todo_list = Todo.objects.all()
    #(username = username)
    #prep course progress
    courses = getAllCourses(username)
    #prep context
    context = {'todo_list' : todo_list, 'courses': courses}
    #render
    return render(request, 'dashboard/todo.html', context)

def add_todo(request):
    #add todo to database
    t = Todo(todo_text=request.POST.get('text', 'no text provided'))
    t.save()
    #redirect to home page
    return HttpResponseRedirect(reverse('dashboard:index'))
