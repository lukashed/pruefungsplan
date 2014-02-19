from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .models import Pruefungsplan, Notification


class SignUpForm(forms.Form):
    pruefungsplan = forms.ModelChoiceField(
        queryset=Pruefungsplan.objects.filter(is_available=False), initial=0,
    )
    email = forms.EmailField()
    phone_number = forms.CharField(
        required=False,
        label='Handynummer',
        help_text='Optional. Wenn angegeben, wirst du per SMS benachrichtigt.\
        Format: z.B. +4915207921346',
        initial='+49',
    )

    helper = FormHelper()
    helper.form_action = '/'
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
