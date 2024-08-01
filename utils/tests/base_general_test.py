import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'exitosa_core.settings'
django.setup()

from django.test import TestCase


class BaseGeneralTest(TestCase):

    def setUp(self):
        pass

