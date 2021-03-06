from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .models import Pruefungsplan, Notification, Exam
from .utils import (
    ExamsByPruefungsplan, BootstrapTextInput, BootstrapEmailInput
)


class ExamSignUpForm(forms.Form):
    exams = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),
        widget=ExamsByPruefungsplan,
    )

    email = forms.EmailField(widget=BootstrapEmailInput)

    def clean_email(self):
        exams = self.cleaned_data['exams']
        print exams
        email = self.cleaned_data.get('email', '')
        if Notification.objects.filter(
            email=email,
            exams__in=exams,
        ).exists():
            raise forms.ValidationError(
                'Diese Email Adresse bekommt bereits eine Benachrichtigung \
                fuer die Klausuren.'
            )
        return email

    phone_number = forms.CharField(
        required=False,
        label='Handynummer',
        help_text='Optional. Wenn angegeben, wirst du per SMS benachrichtigt.\
        Format: z.B. +4915207921346',
        initial='+49',
        widget=BootstrapTextInput,
    )

    def clean_phone_number(self):
        exams = self.cleaned_data['exams']
        number = self.cleaned_data.get('phone_number', '')
        if Notification.objects.filter(
            sms=number,
            exams__in=exams,
        ).exists():
            raise forms.ValidationError(
                'Diese Handynummer Adresse bekommt bereits eine \
                Benachrichtigung fuer die Klausuren.'
            )
        return number

    def draft_notification(self):
        notification = Notification()
        notification.email = self.cleaned_data.get('email', '')

        sms = self.cleaned_data.get('phone_number')
        if sms and sms != '+49':
            notification.sms = sms
        else:
            sms = None

        notification.save()
        notification.exams = self.cleaned_data.get('exams')
        notification.save()

        return notification, sms


class SignUpForm(forms.Form):
    pruefungsplan = forms.ModelChoiceField(
        queryset=Pruefungsplan.objects.filter(is_available=False), initial=0,
    )
    email = forms.EmailField()

    def clean_email(self):
        pruefungsplan = self.cleaned_data['pruefungsplan']
        email = self.cleaned_data.get('email', '')
        if Notification.objects.filter(
            email=email,
            pruefungsplan=pruefungsplan
        ).exists():
            raise forms.ValidationError(
                'Diese Email Adresse bekommt bereits eine Benachrichtigung \
                fuer den Pruefungsplan \
                %s!' % pruefungsplan.name
            )
        return email

    phone_number = forms.CharField(
        required=False,
        label='Handynummer',
        help_text='Optional. Wenn angegeben, wirst du per SMS benachrichtigt.\
        Format: z.B. +4915207921346',
        initial='+49',
    )

    def clean_phone_number(self):
        pruefungsplan = self.cleaned_data['pruefungsplan']
        number = self.cleaned_data.get('phone_number', '')
        if Notification.objects.filter(
            sms=number,
            pruefungsplan=pruefungsplan
        ).exists():
            raise forms.ValidationError(
                'Diese Handynummer bekommt bereits eine Benachrichtigung \
                fuer den Pruefungsplan \
                %s!' % pruefungsplan.name
            )
        return number

    helper = FormHelper()
    helper.form_action = '/pruefungsplan/'
    helper.layout = Layout(
        Field('pruefungsplan', css_class='form-control'),
        Field('email'),
        Field('phone_number'),
        FormActions(
            Submit(
                'save_changes', 'Benachrichtige mich', css_class='btn-primary'
            ),
        )
    )

    def draft_notification(self):
        notification = Notification()

        notification.pruefungsplan = self.cleaned_data.get('pruefungsplan')
        notification.email = self.cleaned_data.get('email', '')

        sms = self.cleaned_data.get('phone_number')
        if sms and sms != '+49':
            notification.sms = sms
        else:
            sms = None

        notification.save()

        return notification, sms
