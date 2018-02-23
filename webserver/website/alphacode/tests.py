from django.test import TestCase
from django.test import Client
# Create your tests here.

from alphacode.models import RandomURLs
from django.utils import timezone
import time

c = Client()
response = c.get('/alphacode/')
assert (response.status_code == 200),"index failed" + str(response.status_code)


response = c.get('/alphacode/test')
assert (response.status_code == 301),"workplace failed" + str(response.status_code)

#Database  General test
print("Generating Test Rows")
r1 = RandomURLs(random_url="eggert",group_name = "f",timestamp=timezone.now(), valid=True)
r1.save()
r2 = RandomURLs(random_url="gegegege",group_name = "f", timestamp=timezone.now(), valid=False)
r2.save()


testRow1 = RandomURLs.objects.get(id=r1.id)
testRow2 = RandomURLs.objects.get(id=r2.id)
assert (testRow1.valid == True)
assert (testRow1.random_url == "eggert")
assert (testRow2.valid == False)
assert (testRow2.random_url == "gegegege")

print("Running URL Expiration Tests")
timespan = 5
print("Timespan is " + str(timespan) + " seconds")
time.sleep(timespan)
assert (testRow1.isExpired(timespan, unit="seconds") == True)
assert (testRow2.isExpired(timespan, unit="seconds") == True)
testRow1.setValidity(False)
assert (testRow1.valid == False)

r1.delete()
r2.delete()



