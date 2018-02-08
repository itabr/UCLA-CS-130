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

    def is_expired(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(days=1)