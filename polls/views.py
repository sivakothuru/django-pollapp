from django.http import HttpResponse
from models import Poll ,Choice
from django.template import Context, loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.contrib.auth.models import User

def login(request):
    f = AuthenticationForm()
    if request.method == 'POST':
        f = AuthenticationForm(None, request.POST)
        if f.is_valid():
            latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
            return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list}, context_instance=RequestContext(request))
        else:
            HttpResponse("Invalid data")
    return render_to_response('polls/login.html',{'form': f}, context_instance=RequestContext(request))


def user_creation(request):
    f = UserCreationForm()
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save(commit=True)
            f = AuthenticationForm()
            return HttpResponseRedirect('/')
        else:
            HttpResponse("Invalid data")
    return render_to_response('polls/user_creation.html', {'form': f}, context_instance=RequestContext(request))

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list}, context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        print request.POST
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        poll = Poll.objects.get(id=poll_id)
        poll.save()
        user = User.objects.get(id=poll.user_id)
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

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                               context_instance=RequestContext(request))

#def votes_regestered(request,id):