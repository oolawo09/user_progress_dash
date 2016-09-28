from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .utils import refreshToken
import requests
from .models import Todo, Course
import math

import logging

# globals for getUser, userExists and getUserCourses
# TODO refactor because they're exposed to other
# functions in this file
token = refreshToken()
authField = "Bearer " + token
headers = {"Authorization": authField}


def getUserName(request):
  # retrieve username from either POST request or cookie

  username = None
  # If request type is POST
  # attempt to retrieve username from POST request data
  if request.method == settings.REQUEST_TYPE_POST:
    username = request.POST.get(settings.USERNAME_COOKIE, None)
    # keep username only if it's valid
    if username != None and len(username) == 0:
      logging.warning("username in post was: %s ", username)
      username = None

  # if method isn't post
  # or username wasn't in POST data
  # attempt to retrieve username from cookie.
  if username == None:
    logging.warning("no username retrieved from POST")
    username = request.session.get(settings.USERNAME_COOKIE, None)

  # if username wasn't in cookie either
  # log warning. User has to submit username first
  if username == None:
    logging.info(
        "username %s retrieved from cookie: submit valid username", username)
    return None
  return username


def getUserProgress(username):
  # get user's course progress bars and overall progress bar

  # get user's courses data from LMS via courses API
  url = settings.COURSE_DETAIL_USER_URL_PREFIX + username
  response = requests.get(url, headers=headers)

  # return none if API call is wrong
  if response.status_code != 200:
    return None

  # draw out all course data
  course_list = response.json()['results']
  data = getCourseData(course_list)
  all_course_data = data[0]

  # and the overall progress in all courses
  # which we use to find the average of progress from all courses
  # that's used to generate the overall_progress string of bars

  total_bars_earned = data[1]
  avg_bars_earned = math.ceil(total_bars_earned / len(all_course_data))

  overall_progress = fillOutOveralProgressBar(
      settings.TOTAL_NUMBER_OF_PROGRESS_BARS, avg_bars_earned)

  return (all_course_data, overall_progress)


def getCourseData(course_list):

  all_course_data = []
  # used to generate total progress string
  total_bars_earned = 0
  for course in course_list:
    course_data = Course(course['number'], course['start'], course['end'])
    all_course_data.append(course_data)
    total_bars_earned += course_data.num_of_bars

  return (all_course_data, total_bars_earned)


def fillOutOveralProgressBar(total_bars, avg_bars_earned):
  user_overall_progress_bar = "["
  i = 0
  while i < total_bars:
    if i < avg_bars_earned:
      user_overall_progress_bar += settings.PROGRESS_BAR_CHARACTER
    else:
      user_overall_progress_bar += settings.PROGRESS_BAR_NO_CHARACTER
    i += 1
  user_overall_progress_bar += "]"
  logging.info("user_overall_progress_bar : %s", user_overall_progress_bar)
  return user_overall_progress_bar


def getUserTodos(username):
  # retrieve only this user's todo items
  todos = []
  all_todos = Todo.objects.all()
  for todo in all_todos:
    if todo.username == username:
      todos.append(todo)
  return todos
