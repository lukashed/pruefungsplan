# coding=utf-8

import requests
import datetime
import uuid
from urlparse import urljoin
from django.db import models
from lxml import html
from .utils import send_email, send_sms



PRUEFUNGSPLAN = 1
EXAM = 2


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
                    notification.send_notification(kind=PRUEFUNGSPLAN)
        else:
            Exam.fetch_exams(self)


MONTH_TO_NUMBER = {
    'Januar': 1,
    'Februar': 2,
    'März': 3,
    'April': 4,
    'Mai': 5,
    'Juni': 6,
    'Juli': 7,
    'August': 8,
    'September': 9,
    'Oktober': 10,
    'November': 11,
    'Dezember': 12,
}

class Exam(models.Model):
    pruefungsplan = models.ForeignKey(
        Pruefungsplan,
        related_name='exams',
    )

    name = models.CharField(max_length=255)
    url = models.URLField()
    date = models.DateField()

    def __unicode__(self):
        return '%s on %s (%s)' % (
            self.name,
            self.date.strftime('%d.%m.%y'),
            self.pruefungsplan,
        )

    @classmethod
    def fetch_exams(cls, pruefungsplan):
        r = requests.get(pruefungsplan.url)

        tree = html.fromstring(r.text)

        dates = tree.xpath('//td[contains(@class, "filled")]')
        for date in dates:
            day = int(date.xpath('h1/text()')[0])
            table = date.getparent().getparent()
            monthyear = table.xpath('caption/text()')[0]
            month_verbose, year = monthyear.split(' ')
            month = MONTH_TO_NUMBER[month_verbose]

            date_python = datetime.date(year=int(year), month=month, day=day)

            exams = date.xpath('ul/li/a')

            for exam in exams:
                url = urljoin(
                    pruefungsplan.url,
                    exam.get('href').encode('utf-8')
                )
                name = exam.text.encode('utf-8')


                try:
                    exam = cls.objects.get(
                        pruefungsplan=pruefungsplan,
                        name=name,
                        url=url,
                    )
                    exam.date = date_python
                    exam.save()
                except cls.DoesNotExist:
                    exam = cls.objects.create(
                        pruefungsplan=pruefungsplan,
                        name=name,
                        url=url,
                        date=date_python,
                    )

    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = self.__class__.objects.get(pk=self.pk)
            if orig.date != self.date:
                for notification in self.notifications.all():
                    notification.send_notification(kind=EXAM, instance=self)

        return super(Exam, self).save(*args, **kwargs)


class Notification(models.Model):
    pruefungsplan = models.ForeignKey(
        Pruefungsplan,
        related_name='notifications',
        blank=True,
        null=True,
    )

    exams = models.ManyToManyField(
        Exam,
        related_name='notifications',
        blank=True,
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

    def send_notification(self, kind, instance=None):
        if kind == PRUEFUNGSPLAN:
            email_subject = 'Pruefungsplan %s ist online!' % (
                self.pruefungsplan.name,
            )
            email_message = 'Der Pruefungsplan %s ist online: %s' % (
                self.pruefungsplan.name,
                self.pruefungsplan.url
            )
            sms_message = 'Pruefungsplan %s ist online!' % (
                self.pruefungsplan.name,
            )
        elif kind == EXAM:
            email_subject = 'Datum der Klausur %s geaendert' % instance.name
            email_message = 'Das Datum der Klausur %s im Pruefungsplan %s \
wurde auf den %s geaendert! Details: %s' % (
    instance.name,
    instance.pruefungsplan.name,
    instance.date.strftime('%d.%m.%y'),
    instance.url
)
            sms_message = 'Datum der Klausur %s wurde auf den %s geaendert' % (
                instance.name,
                instance.date.strftime('%d.%m.%y'),
            )

        if self.email_verified:
            send_email(
                receipient=self.email,
                subject=email_subject,
                message=email_message,
            )
        if self.sms_verified:
            send_sms(
                to=self.sms,
                message=sms_message,
            )
