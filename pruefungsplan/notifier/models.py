import requests
import datetime
import uuid
from django.db import models
from django.conf import settings
from .utils import send_email, send_sms


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
                for notification in self.notifications.all():
                    notification.send_notification()



class Notification(models.Model):
    pruefungsplan = models.ForeignKey(
        Pruefungsplan,
        related_name='notifications'
    )

    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(
        max_length=32,
        default=lambda: uuid.uuid4().hex
    )

    sms = models.CharField(max_length=255, blank=True)
    sms_verified = models.BooleanField(default=False)
    sms_code = models.CharField(
        max_length=4,
        default=lambda: uuid.uuid4().hex[:4]
    )

    def has_sms(self):
        return self.sms and self.sms != '+49'

    def done_confirming(self):
        return (
            self.sms_verified if self.has_sms() else True) \
            and self.email_verified

    password = models.CharField(
        max_length=10,
        default=lambda: uuid.uuid4().hex[:10]
    )

    def __unicode__(self):
        return '%s for %s' % (self.email, self.pruefungsplan)

    def send_notification(self):
        if self.email_verified:
            send_email(
                receipient=self.email,
                subject='Pruefungsplan %s ist online!' % (
                    self.pruefungsplan.name,
                ),
                message='Der Pruefungsplan %s ist online: %s' % (
                    self.pruefungsplan.name,
                    self.pruefungsplan.url
                ),
            )
        if self.sms_verified:
            send_sms(
                to=self.sms,
                message='Pruefungsplan %s ist online!' % (
                    self.pruefungsplan.name,
                ),
            )
