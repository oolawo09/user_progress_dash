from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo
from django.urls import reverse
from .util import getCourseTitles

# Create your views here.
def index(request):
    #prep todos
    todo_list = Todo.objects.all()
    #prep course progress
    course_titles = getCourseTitles(request.POST.get('username', 'no username provided'))
    #prep context
    context = {'todo_list' : todo_list, 'course_titles': course_titles}
    #render
    return render(request, 'dashboard/todo.html', context)

def add_todo(request):
    #add todo to database
    t = Todo(todo_text=request.POST.get('text', 'no text provided'))
    t.save()
    #redirect to home page
    return HttpResponseRedirect(reverse('dashboard:index'))
