from django.conf import settings
from .models import Todo
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
# TODO logging


def addTodo(request):
  # if request isn't post (adding a todo incorrectly?)
  # error message
  if request.method != settings.REQUEST_TYPE_POST:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  # get username stored in session
  username = request.session.get(settings.USERNAME_COOKIE, None)

  # if user hasn't entered username
  # in current session
  if username == None:
    # render blank default page
    context = {settings.ERROR_MESSAGE_KEY,
               "you haven't entered a user name for this session"}
    return index(request, context)

  # if post request doesn't have 'text' key
  # (malformed post ?)
  todo_text = request.POST.get('text', None)
  if todo_text == None:
    context = {settings.ERROR_MESSAGE_KEY,
               "try input the todo again"}
    return index(request, context)

  # create and persist todo with values from get request
  t = Todo(todo_text=todo_text, username=username)
  t.save()

  # redirect to home page
  return HttpResponseRedirect(reverse('dashboard:index'))
