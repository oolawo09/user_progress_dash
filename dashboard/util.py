import requests
import requests.auth
from django.conf import settings
from .models import Course


def refreshToken():
    client_auth = requests.auth.HTTPBasicAuth('602057e53fe4e27eded9', 'b72544f2235e6418e7e027d2856e947f907071c9') #move these vals to config file
    post_data = {"grant_type": "password", "username": "olawo", "password": "oo4423"} #move these vals to config file
    headers = {"User-Agent": "ChangeMeClient/0.1 by olawo"}
    response = requests.post("http://localhost:8000/oauth2/access_token/", auth=client_auth, data=post_data, headers=headers)
    json_resp = response.json()['access_token']
    return json_resp

def getAllCourses(username):
    #throw error if no username is provided
    #needs more rigorous checking of this string's characters and format

    token = refreshToken()
    authField = "Bearer " + token
    headers = {"Authorization" : authField}
    url = "http://localhost:8000/api/courses/v1/courses/?username=" + username
    course_list = requests.get(url, headers=headers)
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
