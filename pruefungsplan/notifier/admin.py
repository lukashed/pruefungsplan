from django.contrib import admin

from .models import Pruefungsplan, Notification


admin.site.register(Pruefungsplan)
admin.site.register(Notification)
