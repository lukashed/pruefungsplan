from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.edit import FormView
from .forms import SignUpForm, ExamSignUpForm
from .models import Notification
from .utils import send_email, send_sms


class ExamSignUpView(FormView):
    kind = 'exam'
    form_class = ExamSignUpForm
    template_name = 'home.html'

    def form_valid(self, form):
        notification, sms = form.draft_notification()

        if sms:
            send_sms(
                sms,
                'Dein Code fuer die Pruefungsplanbenachrichtigung \
                lautet: %s' % (notification.sms_code)
            )

        send_email(
            notification.email,
            'Bitte bestaetige deine Pruefungsplanbenachrichtigung',
            'Wenn du per Email benachrichtigt werden moechtest, \
            klicke bitte auf den folgenden Link: %s' % (
                self.request.build_absolute_uri('/confirm/%s/?mail_code=%s' % (
                    notification.password,
                    notification.email_token
                ))
            )
        )

        self.success_url = '/confirm/%s' % notification.password
        return super(ExamSignUpView, self).form_valid(form)


class SignUpView(FormView):
    kind = 'pruefungsplan'
    form_class = SignUpForm
    template_name = 'home.html'

    def form_valid(self, form):
        notification, sms = form.draft_notification()

        if sms:
            send_sms(
                sms,
                'Dein Code fuer die Pruefungsplanbenachrichtigung \
                lautet: %s' % (notification.sms_code)
            )

        send_email(
            notification.email,
            'Bitte bestaetige deine Pruefungsplanbenachrichtigung',
            'Wenn du per Email benachrichtigt werden moechtest wenn der \
            Pruefungsplan %s online ist, klicke bitte auf den folgenden \
            Link: %s' % (
                notification.pruefungsplan.name,
                self.request.build_absolute_uri('/confirm/%s/?mail_code=%s' % (
                    notification.password,
                    notification.email_token
                ))
            )
        )

        self.success_url = '/confirm/%s' % notification.password
        return super(SignUpView, self).form_valid(form)


def confirm(request, password):
    notification = get_object_or_404(Notification, password=password)

    sms_error = False
    sms_code = request.GET.get('sms_code')
    if sms_code:
        if sms_code == notification.sms_code:
            notification.sms_verified = True
            notification.save()
        else:
            sms_error = True

    mail_error = False
    mail_code = request.GET.get('mail_code')
    if mail_code:
        if mail_code == notification.email_token:
            notification.email_verified = True
            notification.save()
        else:
            mail_error = True

    return render_to_response('confirm.html', {
        'notification': notification,
        'sms_error': sms_error,
        'mail_error': mail_error,
    }, context_instance=RequestContext(request))
