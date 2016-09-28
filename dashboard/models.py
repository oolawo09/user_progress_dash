from django.db import models
from django.conf import settings
from datetime import datetime

import logging
import re


class Todo(models.Model):
  todo_text = models.CharField(max_length=200)
  username = models.CharField(max_length=200, default='')

  def __str__(self):
    return self.todo_text + ":" + self.username


class Course(models.Model):

  def __init__(self,  number, start, end):
    # course number
    self.number = number
    self.start = formatDateTime(start)
    self.end = formatDateTime(end)
    self.percentage = computeProgress(self.start, self.end)

  def __str__(self):
    return self.number


##############################
# utility methods for Course #
##############################

def formatDateTime(date_str):
  # get datetime in new format

  # date_str has to be of UTC time format
  utc_date_time_pattern = re.compile(settings.UTC_DATE_TIME_REGEX_STRING)

  if utc_date_time_pattern.match(str(date_str)) == None:
    logging.error(" %s is not a UTC date time stamp", date_str)
    return None

  return datetime.strptime(date_str, settings.OTHER_DATE_TIME_FORMAT_STRING)


def computeProgress(start, end):
  # award progress bars

  if start == None or end == None:
    return None

  course_duration = end - start
  current_time = datetime.now()
  # number of bars is proportional to the amount of time passed since the
  # course started
  num_of_bars = ((
      current_time - start) / course_duration) * settings.PERCENTAGE
  return int(num_of_bars)
