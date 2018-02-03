from django.test import TestCase
from django.test import Client
# Create your tests here.

c = Client()
response = c.get('/alphacode/')
assert (response.status_code == 200),"index failed" + str(response.status_code)


response = c.get('/alphacode/test')
assert (response.status_code == 301),"workplace failed" + str(response.status_code)
