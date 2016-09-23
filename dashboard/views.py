from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import logging


def index(request, context):
  logging.info("context to be rendered: %s ", context)

  # render view
  return render(request, settings.INDEX_HTML, context)
