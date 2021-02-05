from django.http import HttpResponse
from django.shortcuts import redirect

from django.contrib.auth.models import User


def unauthenticated_User(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def admin_Only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None 
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customers':
            return redirect('user')

        if group == 'admins':
            return view_func(request, *args, **kwargs)
    return wrapper_func