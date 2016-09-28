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
    self.num_of_bars = computeProgress(self.start, self.end)
    self.progress_bar_string = fillBars(self.num_of_bars)

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
    return -1

  course_duration = end - start
  current_time = datetime.now()
  # number of bars is proportional to the amount of time passed since the
  # course started
  num_of_bars = ((
      current_time - start) / course_duration) * settings.TOTAL_NUMBER_OF_PROGRESS_BARS
  return num_of_bars


def fillBars(num_of_bars):
  # fill up progress bars

  # input error check
  if num_of_bars == -1:
    return None

  progress_bars = "["

  i = 0
  while i < settings.TOTAL_NUMBER_OF_PROGRESS_BARS:
    if i < num_of_bars:
      progress_bars += settings.PROGRESS_BAR_CHARACTER
    else:
      progress_bars += settings.PROGRESS_BAR_NO_CHARACTER
    i += 1

  progress_bars += "]"
  return progress_bars
