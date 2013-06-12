"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from polls.models import Poll, Choice
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo",
                                             email="foo@example.com",
                                             password="bar")
        self.c = Client()

    def test_login(self):
        response = self.c.get("/")
        self.assertEqual(200, response.status_code)
        self.c.login(email="foo@example.com", password="bar")
        response = self.c.get("/")
        self.assertEqual(200, response.status_code)

    def test_create_user(self):
        response = self.c.get("/usercreation/")
        self.assertEqual(200, response.status_code)
        self.c.login(email="foo@example.com", password="bar", password1="bar")
        response = self.c.get("/usercreation/")
        self.assertEqual(200, response.status_code)