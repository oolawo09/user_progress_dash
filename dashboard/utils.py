import requests
import requests.auth
from django.conf import settings


def refreshToken():
  # generate a new oauth2 token if last one has expired

  client_auth = requests.auth.HTTPBasicAuth(
      settings.CLIENT_ID, settings.CLIENT_SECRET)  # move these vals to config file
  post_data = {"grant_type": "password", "username": settings.USERNAME,
               "password": settings.PASSWORD}  # move these vals to config file
  user_agent_str = "ChangeMeClient/0.1 by " + settings.USERNAME
  headers = {"User-Agent": user_agent_str}
  response = requests.post(settings.TOKEN_URL_PREFIX,
                           auth=client_auth, data=post_data, headers=headers)
  json_resp = response.json()['access_token']
  return json_resp
