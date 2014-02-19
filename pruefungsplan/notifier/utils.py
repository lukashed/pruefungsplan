import requests
from django.conf import settings
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
