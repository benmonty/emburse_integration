from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

oauth_param_mem_store = [];

# Create your views here.
def index(request):
    return HttpResponse('<a href="https://app.emburse.com/v1/oauth/authorize">Click to Authorize this App</a>')

def callback(request):
    oauth_param_mem_store.append(request.GET.dict())
    oauth_param_mem_store.append({'__TIME__': str(datetime.now())})
    oauth_param_mem_store.append('<br>')
    return HttpResponse(oauth_param_mem_store)
