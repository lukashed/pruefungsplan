from itertools import chain
import requests
from django.conf import settings
from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from twilio.rest import TwilioRestClient


def send_email(receipient, subject, message):
    return requests.post(
        settings.MAILGUN_URL,
        auth=(
            'api', settings.MAILGUN_API_KEY,
        ),
        data={
            'from': 'Pruefungsplan Reminder <lukas@lukasklein.com>',
            'to': receipient,
            'subject': subject,
            'text': message,
        },
    ).text


def send_sms(to, message):
    client = TwilioRestClient(
        settings.TWILIO_SID,
        settings.TWILIO_AUTH_TOKEN
    )
    client.sms.messages.create(
        body=message,
        to=to,
        from_=settings.TWILIO_FROM
    )


class BootstrapTextInput(forms.TextInput):
    def __init__(self, attrs=None):
        return super(BootstrapTextInput, self).__init__({
            'class': 'form-control',
        })

class BootstrapEmailInput(BootstrapTextInput):
    input_type = 'email'


class ExamsByPruefungsplan(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        # I know this is evil but it prevents a circular import loop
        from .models import Pruefungsplan, Exam

        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']

        str_values = set([force_unicode(v) for v in value])
        pruefungsplans = Pruefungsplan.objects.filter(is_available=True)
        for pruefungsplan in pruefungsplans:
            output.append(u'<li>%s</li>'%(pruefungsplan.name))
            output.append(u'<ul>')
            del self.choices
            self.choices = []
            exams = Exam.objects.filter(pruefungsplan=pruefungsplan)
            for exam in exams:
                self.choices.append((exam.id, exam.name))
            for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''
                cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
            output.append(u'</ul>')
            output.append(u'</li>')
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))
