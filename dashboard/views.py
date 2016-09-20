from django.shortcuts import render
from django.http import HttpResponse
from .models import Todo 

# Create your views here.
def index(request): 
    return HttpResponse("Hello, world. You're at the polls index.")


def todo(request):
    todo_list = Todo.objects.all()
    print(todo_list)
    context = {'todo_list' : todo_list}
    return render(request, 'dashboard/todo.html', context)
