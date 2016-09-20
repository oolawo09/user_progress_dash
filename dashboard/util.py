import requests
import requests.auth
from django.conf import settings

def refreshToken():
    client_auth = requests.auth.HTTPBasicAuth('602057e53fe4e27eded9', 'b72544f2235e6418e7e027d2856e947f907071c9') #move these vals to config file
    post_data = {"grant_type": "password", "username": "olawo", "password": "oo4423"} #move these vals to config file
    headers = {"User-Agent": "ChangeMeClient/0.1 by olawo"}
    response = requests.post("http://localhost:8000/oauth2/access_token/", auth=client_auth, data=post_data, headers=headers)
    json_resp = response.json()['access_token']
    return json_resp

def getCourseTitles(username):
    token = refreshToken()
    authField = "Bearer " + token
    headers = {"Authorization" : authField}
    course_list = requests.get("http://localhost:8000/api/courses/v1/courses/?username=olawo", headers=headers)
    course_list = course_list.json()['results']
    course_titles = []
    for course in course_list :
        course_titles.append(course['course_id'])
    return course_titles
