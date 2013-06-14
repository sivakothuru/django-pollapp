from django.http import HttpResponse
from polls.models import Poll ,Choice, Vote
from django.template import Context, loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list}, context_instance=RequestContext(request))

@login_required
def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

@login_required
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        poll = Poll.objects.get(id=poll_id)
        poll.save()
        user = request.user
        try:
            voter = Vote.objects.get(user=user, poll=poll)
            voter.choice = selected_choice
            voter.save()
        except:
            vote = Vote.objects.create(user=user, poll=poll, choice=selected_choice)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

@login_required
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                               context_instance=RequestContext(request))



def votes_of_a_user(request, poll_id):
    try:
       voter = request.user.user_votes.get(poll__id=poll_id)
       name = voter.user.username
       poll = voter.poll.question
       choice = voter.choice.choice_text
       p = get_object_or_404(Poll, pk=poll_id)
    except:
       msg = 'You already deleted this vote so please vote again '
       latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
       return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list, 'msg':msg}, context_instance=RequestContext(request))         


    return render_to_response('polls/votes_of_user.html',
                              {'name':name, 'polled':poll,'choice':choice,
                              'poll': p},
                              context_instance=RequestContext(request))

def deleting_vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    voter = request.user.user_votes.get(poll__id=poll_id)
    voter.choice.votes -= 1
    voter.choice.save()
    voter = request.user.user_votes.get(poll__id=poll_id).delete()
    return render_to_response('polls/results.html', {'poll':p},
                              context_instance=RequestContext(request))

def polls_with_most_votes(request):
    p = Choice.objects.all().order_by('votes')[:5]
    #import pdb;pdb.set_trace()
    return HttpResponse("highest vote polls")