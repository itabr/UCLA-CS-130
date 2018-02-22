from django.shortcuts import render , redirect
from django.http import HttpResponse
import string
import random
import json
import time
import threading


from alphacode.models import RandomURLs
from django.utils import timezone
  

#alphacode/
def index(request):
    context = {
    }
    return render(request,'alphacode/index.html',context)

#create/
def create(request):
    groupName = request.GET.get('name')
    N = 16
    while True:
        random_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
        try:
            row = RandomURLs.objects.get(random_url=random_string)
        except RandomURLs.DoesNotExist:
            break  
    Row = RandomURLs(random_url=random_string, group_name=groupName, timestamp=timezone.now(), valid=True)
    Row.save()
    return redirect('workplace-view', workplace_id=random_string)

#alphacode/(workplace_id)
def workplace(request,workplace_id):
    try:
        groupName = RandomURLs.objects.get(random_url=workplace_id)
    except RandomURLs.DoesNotExist:
        return redirect('error-view')
    context = {
        "workplace_id": workplace_id,
        "group_name"  : groupName.group_name,
    }
    return render(request,'alphacode/workplace.html',context)


def getTag(request):
    #       run ML function for the tag here
    #       input string
    #       output string
    data = request.GET.get('Smt')
    # json data is just a JSON string now. 
    return HttpResponse(data)
        

def error_page(request):
    context = {
    }
    return render(request,'alphacode/error.html',context)