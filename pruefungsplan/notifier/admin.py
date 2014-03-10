from django.contrib import admin

from .models import Pruefungsplan, Notification, Exam


admin.site.register(Pruefungsplan)
admin.site.register(Notification)
admin.site.register(Exam)
