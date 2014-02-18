import requests
import datetime
from django.db import models


class Pruefungsplan(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    is_available = models.BooleanField(default=False)
    available_since = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def update(self):
        if not self.is_available:
            r = requests.get(self.url)
            html = r.text

            available = 'class="month"' in html

            if available:
                self.is_available = True
                self.available_since = datetime.datetime.now()
                self.save()
