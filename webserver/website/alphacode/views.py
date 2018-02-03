from django.shortcuts import render , redirect
from django.http import HttpResponse

#alphacode/
def index(request):
    context = {
    }
    return render(request,'alphacode/index.html',context)

#alphacode/(workplace_id)
def workplace(request,workplace_id):
    context = {
		"workplace_id": workplace_id
    }
    return render(request,'alphacode/workplace.html',context)
