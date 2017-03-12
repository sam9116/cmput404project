from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login



# Create your views here.

def register(request):
    """ registers new user"""
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'register.html',
        {
            'title':'Please Register',
            'message':'You need to register before using our service',
            'year':datetime.now().year,
        }
)



def linknothome(request):
    """ homepage of linknot"""
    assert isinstance(request,HttpRequest)
    if not request.user.is_authenticated:
       return redirect('/login/')
    else:
       return render(
        request,
        'linknot_home.html',
        {
            'title':'Welcome',
            'username':request.user.username,
            'message':'Your Feed',
            'year':datetime.now().year,
        }
        )

def login_user(request):
    """login for users"""
    #todo check csrf token
    assert isinstance(request,HttpRequest)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)
    #http://cheng.logdown.com/posts/2016/01/06/django-create-and-login-user-manually



    if user is not None:
    # A backend authenticated the credentials
        login(request, user)
        return redirect('/')
    else:
        return render(request,
                      'login.html',
                      {
                      'title':'login',
                      'message':'Login please',
                      'year':datetime.now().year,
                      }
                  )
