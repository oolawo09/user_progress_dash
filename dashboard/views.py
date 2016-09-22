from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import logging


def index(request, context):
  logging.info("context to be rendered: %s ", context)

  # render view
  return render(request, 'dashboard/todo.html', context)
