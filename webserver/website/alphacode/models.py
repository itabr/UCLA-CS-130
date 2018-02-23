import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class RandomURLs(models.Model):
    id = models.AutoField(primary_key=True)
    random_url = models.CharField(max_length=20)
    group_name = models.CharField(max_length=30)
    timestamp = models.DateTimeField()
    valid = models.BooleanField()

    def __str__(self):
        return self.random_url

    def isExpired(self, timespan, unit="hour"):
        '''
        Inputs:
        timespan: The lasting time for URL
        unit: The unit for lasting time, the default unit is hour
              The seconds mode is for testing
        Output:
        True if the current time exceeds the timespan of URL
        False otherwise 
        '''
        timediff = 0
        if (unit == "hour"):
            timediff = datetime.timedelta(hours=timespan)
        elif (unit == "seconds"):
            timediff = datetime.timedelta(seconds=timespan)

        #print(timediff)
        #print(timezone.now() - self.timestamp)
        return  timediff <= timezone.now() - self.timestamp

    def setValidity(self, validity):
        '''
        Inputs:
           validity (Boolean) : Set the validity of the URL
        '''
        self.valid = validity
        self.save()