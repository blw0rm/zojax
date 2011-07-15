### -*- coding: utf-8 -*- ####################################################

from zojax.settings import *
from django.conf import global_settings


# We don't need to use S3 for test purposes. These functionality
# should be tested in appropriate application
DEFAULT_FILE_STORAGE = global_settings.DEFAULT_FILE_STORAGE

