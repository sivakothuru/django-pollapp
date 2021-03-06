"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
Replace this with more appropriate tests for your application.
"""

import datetime

from django.utils import timezone
from django.test import TestCase
from django.test import Client
from polls.models import Poll, Choice, Vote
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
        choice = Choice.objects.create(poll=poll, choice_text='not much')
        response = self.c.post(reverse('vote', args=[poll.id]), {'choice':choice.id})
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.post(reverse('vote', args=[poll.id]), {'choice':choice.id})

        self.assertEqual(302, response.status_code)
        response = self.c.post(reverse('vote', args=[poll.id]), {'choice':choice.id})
        self.assertEqual(302, response.status_code)
        response = self.c.post(reverse('vote', args=[poll.id]), {})
        error_message = "You didn't select a choice."
        self.assertEqual(response.context['error_message'], error_message)
        #vote = Vote.objects.create(user=self.user, poll=poll, choice=choice)
        #vote = Vote.objects.get(poll=poll.id)
        #self.assertEqual( )
    
    def test_votes_of_a_user(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        choice = Choice.objects.create(poll=poll, choice_text='not much')
        vote = Vote.objects.create(user=self.user, poll=poll, choice=choice)
        self.c.login(username="foo", password="bar")
        response = self.c.get(reverse('myvotes', args=[poll.id]))
        self.assertEqual(200, response.status_code)
        name = vote.user.username
        self.assertEqual(response.context["name"], name)
        response = self.c.get(reverse('myvotes', args=[10]))
        msg = "You already deleted this vote so please vote again "
        self.assertEqual(response.context["msg"], msg)



    def test_deleting_vote(self):
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        choice = Choice.objects.create(poll=poll, choice_text='not much')
        vote = Vote.objects.create(user=self.user, poll=poll, choice=choice)
        response = self.c.get("/deleting_vote/")
        self.assertEqual(302, response.status_code)
        self.c.login(username="foo", password="bar")
        response = self.c.post(reverse('deleting'), {'poll_id':vote.poll.id})
        self.assertEqual(200, response.status_code)

    def test_polls_with_most_votes(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/highest_votes_rcvd_polls/")
        self.assertEqual(200, response.status_code)
        poll = Poll.objects.create(user=self.user, question='wts up?',pub_date=datetime.datetime.now())
        choice = Choice.objects.create(poll=poll, choice_text='not much')
        vote = Vote.objects.create(user=self.user, poll=poll, choice=choice)
        poll = Poll.objects.create(user=self.user, question='hi how r u?',pub_date=datetime.datetime.now())
        choice = Choice.objects.create(poll=poll, choice_text='i am fine!')
        vote = Vote.objects.create(user=self.user, poll=poll, choice=choice)
        newA = {"wts up?": {'not much':1}, "hi how r u?": {'i am fine!':1}}
        response = self.c.get("/highest_votes_rcvd_polls/")
        self.assertEqual(response.context['fulldata'], newA)

    def test_polls_and_votes_of_user(self):
        self.c.login(username="foo", password="bar")
        response = self.c.get("/polls_and_votes/")
        self.assertEqual(200, response.status_code)