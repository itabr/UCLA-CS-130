from django.shortcuts import render , redirect
from django.http import HttpResponse
import string
import random
import json
from django.views.decorators.csrf import requires_csrf_token

#alphacode/
def index(request):
    context = {
    }
    return render(request,'alphacode/index.html',context)

#create/
def create(request):
	N = 16
	temp = ""
	random_string = ''.join(random.choice( string.ascii_letters + string.digits) for _ in range(N))
	return redirect('workplace-view', workplace_id=random_string)

#alphacode/(workplace_id)
def workplace(request,workplace_id):
    context = {
		"workplace_id": workplace_id
    }
    return render(request,'alphacode/workplace.html',context)

@requires_csrf_token
def ajax(request):
	if request.method == 'POST':
	#		run ML function for the tag here
	#		input string
	#		output string
		result = "whatever the tag is"
	return HttpResponse(json.dumps({'tag': result}), content_type='application/json')
