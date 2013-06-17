"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from polls.models import Poll, Choice
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class SimpleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo",
                                             email="foo@example.com",
                                             password="bar")
        self.c = Client()

    def test_login(self):
        response = self.c.get("/")
        self.assertEqual(200, response.status_code)

        response = self.c.post("/", {'username':"foo", 'password':"bar"})
        self.assertEqual(200, response.status_code)

    def test_create_user(self):
        response = self.c.get("/usercreation/")
        self.assertEqual(200, response.status_code)
        response = self.c.post("/usercreation/", {'email':"foo@example.com", 'password1':"bar", 'password2':"bar"})
        self.assertEqual(200, response.status_code)
        data = {'username':"foo@example.com", 'password1':"bar", 'password2':"bar"}
        form = UserCreationForm(data)
        self.assertEqual(form.is_valid(), True)
        data = {}
        form = UserCreationForm(data)
        self.assertEqual(form.is_valid(), False)

    def test_logout(self):
        response = self.c.get("/logout/")
        self.assertEqual(200, response.status_code)