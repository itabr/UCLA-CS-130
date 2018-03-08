from django.shortcuts import render , redirect
from django.http import HttpResponse
import string
import random
import json
import time
import threading


from alphacode.models import RandomURLs
from django.utils import timezone
  
from alphacode.machine_learning import tag


#alphacode/
def index(request):
    return render(request,'alphacode/index.html')

#create/
def create(request):
    groupName = "alphacode"
    N = 16
    random_string = ''.join(random.choice(string.digits) for _ in range(N))
    return redirect(workplace, workplace_id=random_string)


def createapi(request):
    groupName = "alphacode"
    N = 16
    random_string = ''.join(random.choice(string.digits) for _ in range(N))
    return HttpResponse(random_string)

#alphacode/(workplace_id)
def workplace(request,workplace_id):
    # try:
    #     groupName = RandomURLs.objects.get(random_url=workplace_id)
    # except RandomURLs.DoesNotExist:
    #     return redirect('error-view')
    context = {
        "workplace_id": workplace_id,
        # "group_name"  : groupName.group_name,
    }
    return render(request,'alphacode/workplace.html',context)

def getTag(request):
    #       run ML function for the tag here
    #       input string
    #       output string
    data = request.GET.get('Smt')
    print(tag.tag(data))
    # print(tag.tag(data))
    # json data is just a JSON string now. 
    return HttpResponse(tag.tag(data))

def error_page(request):
    context = {
    }
    return render(request,'alphacode/error.html',context)