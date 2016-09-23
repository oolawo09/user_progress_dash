from django.conf import settings

# initialise logger
# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.basicConfig(level=logging.DEBUG)
