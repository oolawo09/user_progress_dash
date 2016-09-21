import requests
from django.conf import settings
from .models import Course
from .utils import refreshToken




def getAllCourses(username):
    #throw error if no username is provided
    #needs more rigorous checking of this string's characters and format

    token = refreshToken()
    authField = "Bearer " + token
    headers = {"Authorization" : authField}
    url = "http://localhost:8000/api/courses/v1/courses/?username=" + username
    course_list = requests.get(url, headers=headers)
    print(course_list.json())
    course_list = course_list.json()['results']
    courses = []
    for course in course_list :
        courses.append(getCourse(course['id'], headers))
    return courses


def getCourse(id, headers):
    url = "http://localhost:8000/api/courses/v1/courses/" + id
    course_details = requests.get(url, headers=headers)
    course_details = course_details.json()
    course = Course(course_details['number'], course_details['start'], course_details['end'])
    return course
