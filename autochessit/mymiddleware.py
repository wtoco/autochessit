from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
import re


class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        print(request.path)

        if request.path == '/accounts/login/' or re.match('^/admin', request.path) != None:
            pass
        else:
            if user.is_authenticated():
                pass
            else:
                return HttpResponseRedirect('/accounts/login/')