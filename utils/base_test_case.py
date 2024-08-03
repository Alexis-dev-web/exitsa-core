import os
import django

from django.test import TestCase

from rest_framework.test import APIClient

os.environ['DJANGO_SETTINGS_MODULE'] = 'exitosa_core.settings'
django.setup()

class BaseCase(TestCase):

    def setUp(self):
        self.client = APIClient()
