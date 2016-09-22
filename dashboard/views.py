from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Todo
from django.urls import reverse
from .controllers import getUserName, getUserCourses, getPendingTodos
from django.conf import settings

# This is a single view app.
# index() renders that view.
def index(request):
  # Initialise username
  username = getUserName()

  # if username == None,
  # render the view with neither todo list
  # nor any course progress data.
  # because user doesn't exist
  if username == None:
    return render(request, 'dashboard/todo.html', None)

  # throw error if username doesn't exist in LMS

  # else
  # get global todo_list

  # TODO optimise by getting user's
  #todo instead of global todo list###

  all_todos = Todo.objects.all()
  # get current user's todos
  user_todos = getUserTodos(all_todos, username)
  # get pending ones
  user_pending_todos = getPendingTodos(user_pending_todos)

  # get  user's course progress data
  courses = getUserCourses(username)

  # feed to do list
  # and course progress data
  # into context
  context = {'todo_list': todo_list, 'courses': courses}

  # render a response
  response = render(request, 'dashboard/todo.html', context)

  # Finally, set the username in the cookie
  # for the next request before returning the response object

  # set settings.COOKIENAME cookie to username
  request.sessions[settings.COOKIE_NAME] = username

  return response
