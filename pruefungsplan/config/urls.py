# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from notifier.views import ExamSignUpView, SignUpView, confirm


urlpatterns = patterns('',
    url(r'^$',
        ExamSignUpView.as_view(),
        name="home"),
    url(r'^pruefungsplan/$',
        SignUpView.as_view(),
        name="pruefungsplan"),
    url(r'^confirm/(?P<password>[a-f0-9]{10})/$', confirm),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^impressum/$',
        TemplateView.as_view(template_name='pages/imprint.html'),
        name="imprint"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Your stuff: custom urls go here

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
