from django.db import models
from django.conf import settings
from datetime import datetime

import re
import logging


class Todo(models.Model):
  todo_text = models.CharField(max_length=200)
  username = models.CharField(max_length=200, default='')

  def __str__(self):
    return self.todo_text + ":" + self.username


class Course(models.Model):

  def __datetime(self, date_str):
    # get the date in new format #TODO: what is the name of this format
    return datetime.strptime(date_str, settings.OTHER_DATE_TIME_FORMAT_STRING)

  def __init__(self,  number, start, end):
    # course number
    self.number = number

    # only working with type UTC timestamp
    utc_date_time_pattern = re.compile(settings.UTC_DATE_TIME_REGEX_STRING)

    # check if start time follows UTC format
    if utc_date_time_pattern.match(str(start)) == None:
      logging.error(" start %s is not a UTC date time stamp", start)
      # use this as an error flag when rendering
      self.num_of_progress_bars_awarded = -1
      return None

    # check if end time follows UTC format
    if utc_date_time_pattern.match(str(end)) == None:
      logging.error(" end %s is not a UTC date time stamp", end)
      # use this as an error flag when rendering
      self.num_of_progress_bars_awarded = -1
      return None

    # if both start and end are UTC format, assign correctly and calculate
    # number of progress bars
    self.start = self.__datetime(start)
    self.end = self.__datetime(end)
    self.progress_bars = self.computeProgress(self.start, self.end)

  def computeProgress(self, start, end):
    # award progress bars
    course_duration = end - start
    resized_course_duration = course_duration
    current_time = datetime.now()
    self.num_of_progress_bars_awarded = ((
        current_time - self.start) / course_duration) * settings.TOTAL_NUMBER_OF_PROGRESS_BARS

    # fill up progress bars
    progress_bars = "["

    logging.info("total number of bars %d",
                 settings.TOTAL_NUMBER_OF_PROGRESS_BARS)
    logging.info("progress bars awarded %d", self.num_of_progress_bars_awarded)

    i = 0
    while i < settings.TOTAL_NUMBER_OF_PROGRESS_BARS:
      if i < self.num_of_progress_bars_awarded:
        progress_bars += settings.PROGRESS_BAR_CHARACTER
      else:
        progress_bars += settings.PROGRESS_BAR_NO_CHARACTER
      i += 1

    progress_bars += "]"

    logging.info("progress bars: %s", progress_bars)
    return progress_bars

  def __str__(self):
    return self.number
