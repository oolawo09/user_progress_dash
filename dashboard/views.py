import requests
import urllib.parse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Todo, Course
from .controller import getUserName, getUser, userExistsInLMS, getUserCoursesProgressData, fillOutOveralProgressBar,  getUserTodos
import logging
import math
from django.shortcuts import render


# TODO write unit tests

# render index view
def index(request):
  # Initialise username from either request (user just entered username)
  # or cookie (user's entered a username in this session)
  username = getUserName(request)

  # if username wasn't found then render error view
  if username == None:
    logging.error("username for this session not set yet")
    context = {settings.ERROR_MESSAGE_KEY:
               "username for this session not set yet"}
    return render(request, settings.INDEX_HTML, context)

  # TODO should I block username of value ''? is '' a valid username ?
  # set the username in the cookie
  # for the next request before returning the response object
  logging.info("username %s set in session cookie", username)
  request.session[settings.USERNAME_COOKIE] = username

  # get current user's todos
  user_todos = getUserTodos(username)

  # get  user's course progress data
  progress = getUserCoursesProgressData(username)

  # if progress not received, render error message
  if progress == None:
    logging.error("progress for %s not received from LMS", username)
    context = {settings.ERROR_MESSAGE_KEY:
               "progress not received from LMS"}
    return render(request, settings.INDEX_HTML, context)
  course_progress = progress[0]
  overall_progress = progress[1]

  # feed to do list
  # and course progress data
  # into context
  context = {'username': username, 'todo_list': user_todos,
             'courses': course_progress, 'overall_progress': overall_progress}
  logging.info("context to be rendered: %s ", context)

  # render a response
  return render(request, settings.INDEX_HTML, context)


def addTodo(request):
  # if request isn't post
  # render error message
  if request.method != settings.REQUEST_TYPE_POST:
    return HttpResponseNotFound('<h1>Page not found</h1>')

  # get username stored in session
  username = request.session.get(settings.USERNAME_COOKIE, None)

  # if user hasn't entered username in current session
  if username == None:
    # render error message
    context = {settings.ERROR_MESSAGE_KEY,
               "you haven't entered a username for this session"}
    return index(request, context)

  # if post request doesn't have 'text' key
  todo_text = request.POST.get('text', None)
  if todo_text == None:
    context = {settings.ERROR_MESSAGE_KEY,
               "try inputing the todo again"}
    # render error message
    logging.info("context to be rendered: %s ", context)
    return render(request, settings.INDEX_HTML, context)

  # create and persist todo with values from get request
  t = Todo(todo_text=todo_text, username=username)
  t.save()

  # redirect
  return HttpResponseRedirect(reverse('dashboard:index'))


def completeTodo(request):
  # retrieve todo by todo_id
  # TODO # make sure todo_id is valid and exist in DB
  # delete it
  todo_id = request.POST.get('id', None)
  todo = Todo.objects.get(id=todo_id)

  if todo != None:
    logging.info("Marking todo with id %s as done", todo_id)
    todo.delete()
  else:
    logging.warning("todo with id %s doesn't exist", todo_id)

  # redirect to home page
  return HttpResponseRedirect(reverse('dashboard:index'))
