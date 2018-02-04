from django.test import TestCase
from django.test import Client
# Create your tests here.

from alphacode.models import RandomURLs
from django.utils import timezone
c = Client()
response = c.get('/alphacode/')
assert (response.status_code == 200),"index failed" + str(response.status_code)


response = c.get('/alphacode/test')
assert (response.status_code == 301),"workplace failed" + str(response.status_code)

#Database test
r1 = RandomURLs(random_url="eggert", timestamp=timezone.now(), valid=True)
r1.save()
r2 = RandomURLs(random_url="gegegege", timestamp=timezone.now(), valid=False)
r2.save()

assert (RandomURLs.objects.get(id=r1.id).valid == True)
assert (RandomURLs.objects.get(id=r1.id).random_url == "eggert")
assert (RandomURLs.objects.get(id=r2.id).valid == False)
assert (RandomURLs.objects.get(id=r2.id).random_url == "gegegege")

r1.delete()
r2.delete()

