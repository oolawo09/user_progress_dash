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
  username = None
  # If request type is POST (username has been entered)
  # attempt to retrieve username from POST request data
  if request.method == settings.REQUEST_TYPE_POST:
    username = request.POST.get(settings.USERNAME_COOKIE, None)
    # keep username only if it's valid
    if username != None and len(username) == 0:
      logging.warning("username in post was: %s ", username)
      username = None

  # if method wasn't post (username wasn't entered)
  # or username wasn't in POST data (malformed POST request ?)
  # attempt to retrieve username from cookie. (we're staying maintaining
  # current session as was)
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


def getUser(username):
  # insert username into url
  url = settings.USERS_API_URL_PREFIX % username
  # url = urllib.parse.quote(unencoded_url_string, safe='')
  # print("\n\n\nurl\n\n\n"+url)
  # get user data from LMS via users api
  logging.debug("url get: %s", url)
  response = requests.get(url, headers=headers)
  # raise exception for bad http responses
  # return None
  if response.status_code != 200:
    response.raise_for_status
    logging.warning("failed to get user data from LMS")
    return None

  # TODO: testing. what types of responses could I get here
  # how to handle each
  return response


def userExistsInLMS(username):
  user_dict = getUser(username)

  # if getUser returns None
  # return false
  if user_dict == None:
    logging.warning("user doesn't exist")
    return False

  # if user_dict contains 'name' key
  # user exists
  logging.debug("user object: %s ", user_dict)
  return user_dict.json()[settings.USER_EXISTS_CHECKER_KEY] != None


def getUserCoursesProgressData(username):
  # throw error if user with username doesn't exist

  url = settings.COURSE_DETAIL_USER_URL_PREFIX + username
  # get user's courses data from LMS via courses API
  response = requests.get(url, headers=headers)

  # TODO: testing. what types of responses could I get here
  # how to handle those cases
  if response.status_code != 200:
    return None

  users_course_list = response.json()['results']
  course_progress_bars = []

  total_bars_earned = 0

  for course in users_course_list:
    # filter out progress data while filling total progress bar
    course_progress_data = getCourseProgressBars(course)
    course_progress_bars.append(course_progress_data)
    # compute total progress
    total_bars_earned += course_progress_data.num_of_progress_bars_awarded

  avg_bars_earned = math.ceil(total_bars_earned / len(course_progress_bars))
  logging.info("avg_bars_earned : %s", avg_bars_earned)

  logging.info("total_bars : %s", settings.TOTAL_NUMBER_OF_PROGRESS_BARS)

  user_overal_progress_data = fillOutOveralProgressBar(
      settings.TOTAL_NUMBER_OF_PROGRESS_BARS, avg_bars_earned)
  logging.info("user_overal_progress_data : %s", user_overal_progress_data)

  return (course_progress_bars, user_overal_progress_data)


# fill out overall progress bar
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


def getCourseProgressBars(course):
  # get and return course number, start date and enddate
  course_progress_data = Course(
      course['number'], course['start'], course['end'])
  return course_progress_data


def getUserTodos(username):
  # TODO retrieve only this user's todo items
  todos = Todo.objects.all()
  for todo in todos:
    if todo.username != username:
      todo.delete()
  return todos
