# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from polls.models import Poll
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


def login_view(request):
    f = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        f = AuthenticationForm(None, request.POST)
        if f.is_valid():
            username = f.get_user()
            login(request, username)
            latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
            return render_to_response('polls/index.html',
                                      {'latest_poll_list': latest_poll_list},
                                       context_instance=RequestContext(request))
    return render_to_response('authdetails/login.html', {'form': f},
                              context_instance=RequestContext(request))


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
    return render_to_response('authdetails/user_creation.html',
                              {'form': f},
                               context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    f = AuthenticationForm()
    return render_to_response("authdetails/login.html",
                              {'form': f},
                               context_instance=RequestContext(request))
