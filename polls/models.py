from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Poll(models.Model):
    user = models.ForeignKey(User, related_name="user_polls", null=True, blank=True)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created = models.DateTimeField('created date', default = datetime.datetime.now())
    updated = models.DateTimeField('updated date', auto_now=True)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text

class Vote(models.Model):
    user = models.ForeignKey(User, related_name="user_votes", null=True, blank=True)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice, related_name='selected_choice')