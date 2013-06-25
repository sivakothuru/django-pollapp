"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_MorrisDemo(self):
         self.client.get(reverse('demo_morris_demo'))
