"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
Replace this with more appropriate tests for your application.
"""

import datetime

from django.utils import timezone
from django.test import TestCase
from django.test import Client
from polls.models import Poll, Choice
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse 

class PollMethodTests(TestCase):

    def test_was_published_recently_with_future_poll(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return False for polls whose pub_date
        is older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return True for polls whose pub_date
        is within the last day
        """
        recent_poll = Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)

class TestViewsBasic(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="foo",
                                             email="foo@example.com",
                                             password="bar")
        self.c = Client()

    def test_index(self):
        response = self.c.get("/index/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get("/index/")
        self.assertEqual(200, response.status_code)


    def test_detail(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        response = self.c.get(reverse('detail', args=[poll.id]))
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get(reverse('detail', args=[poll.id]))
        self.assertEqual(200, response.status_code)

    def test_results(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        response = self.c.get(reverse('results', args=[poll.id]))
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get(reverse('results', args=[poll.id]))
        self.assertEqual(200, response.status_code)


    def test_vote(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        response = self.c.get(reverse('vote', args=[poll.id]))
        self.assertEqual(302, response.status_code)
        choice = Choice.objects.create(poll=poll, choice_text='not much')
        response = self.c.post(reverse('vote', args=[poll.id]), {choice:choice.id})
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.get(reverse('vote', args=[poll.id]))
        self.assertEqual(200, response.status_code)
        response = self.c.post(reverse('vote', args=[poll.id]), {choice:choice.id})
        self.assertEqual(200, response.status_code)
    
    def test_votes_of_a_user(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        response = self.c.get(reverse('myvotes', args=[poll.id]))
        self.assertEqual(200, response.status_code)

    def test_deleting_vote(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        response = self.c.get("/deleting_vote/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.post(reverse('deleting'), {'poll_id':poll.id}) 
        self.assertEqual(200, response.status_code)

    def test_polls_with_most_votes(self):
        response = self.c.get("/highest_votes_rcvd_polls/")

        self.assertEqual(200, response.status_code)