import requests
from django.conf import settings
from .models import Course
from .utils import refreshToken

##globals for getUser, userExists and getUserCourses
##TODO refactor because they're exposed to other
#functions in this file
token = refreshToken()
authField = "Bearer " + token
headers = {"Authorization": authField}

def getUser(username):
    url = settings.USERS_API_URL_PREFIX + username
    #get user data from LMS via users api
    response = requests.get(url, headers=headers)
    return response.json()

def userExists(username):
    return getuser(username, )[settings.USEREXISTS_CHECKER_KEY] != None

def getUserCourses(username):
  #throw error if user with username doesn't exist
  if userExists(username) == False:
      ##TODO log this error
      raise ValueError("user by username '+ username + ' doesn't exist in the LMS")

  url = settings.COURSE_DETAIL_USER_URL_PREFIX + username
  #get user's courses data from LMS via courses API
  response = requests.get(url, headers=headers)
  users_course_list =response.json()['results']
  user_courses_progress_data = []

  for course in users_course_list:
    #filter out progress data
    user_courses_progress_data.append(getCourse(course))

  return user_courses_progress_data

def getCourse(course):
  #get and return course number, start date and enddate
  course_progress_data = Course(course['number'], course['start'], course['end'])
  return course_progress_data


def addTodo(request):
  # create the todo
  t = Todo(todo_text=request.POST.get('text', ''), username=request.sessions[settings.USERNAME_COOKIE])
  t.save()
  # redirect to home page
  return HttpResponseRedirect(reverse('dashboard:index'))

def getPendingTodos(todos):
  for todo in todos:
    # delete's all the user's complete todos
    if todo.done:
      todo.delete()
  return todos

def getUserTodos(todos, name):
  tasks = []
  for todo in todos:
    # filter by name
    if todo.username == name:
      tasks.append(todo)
  return tasks


def getUserName(request):
  username = None
  # If request type is POST
  # attempt to retrieve username from POST request data
  if request.method == settings.REQUEST_TYPE_POST:
    username = request.POST.get(settings.USERNAME_COOKIE, None)

  # if username wasn't in POST data
  # attempt to retrieve it from cookie.
  if username == None:
    username = request.sessions.get(settings.USERNAME_COOKIE, None)

  return username
