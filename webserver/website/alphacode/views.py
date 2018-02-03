from django.shortcuts import render , redirect
from django.http import HttpResponse
import string
import random
#alphacode/
def index(request):
    context = {
    }
    return render(request,'alphacode/index.html',context)

#create/
def create(request):
	N = 16
	random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

	return redirect('workplace-view', workplace_id=random_string)

#alphacode/(workplace_id)
def workplace(request,workplace_id):

    context = {
		"workplace_id": workplace_id
    }
    return render(request,'alphacode/workplace.html',context)
