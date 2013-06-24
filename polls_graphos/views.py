# Create your views here
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from graphos.renderers import morris
from graphos.sources.model import ModelDataSource
from polls.models import Vote, Poll, Choice
import json
import time
import urllib2
import datetime


class MorrisDemo(TemplateView):
    template_name = 'polls_graphos/morris.html'
    renderer = None

    def get_context_data(self, **kwargs):
        super_context = super(MorrisDemo, self).get_context_data(**kwargs)
        queryset = Choice.objects.all() 
        data_source = ModelDataSource(queryset,
                                      fields=['choice_text', 'votes'])
        line_chart = self.renderer.LineChart(data_source,
                                      options={'choice_text': "votes"})
        bar_chart = self.renderer.BarChart(data_source,
                                    options={'choice_text': "votes"})
        context = {"line_chart": line_chart,
                   'bar_chart': bar_chart}
        context.update(super_context)
        return context

morris_demo = MorrisDemo.as_view(renderer=morris)


