import os
import django
import uuid

from django.test import TestCase
from unittest.mock import patch, Mock
from django.urls import reverse

os.environ['DJANGO_SETTINGS_MODULE'] = 'exitosa_core.settings'
django.setup()

from rest_framework.test import APIClient

from user.models import User