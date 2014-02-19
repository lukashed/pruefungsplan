# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Notification'
        db.create_table(u'notifier_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pruefungsplan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Pruefungsplan'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('email_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_token', self.gf('django.db.models.fields.CharField')(default='2be86a2506c94506bd6758fd62a82920', max_length=32)),
            ('sms', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sms_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sms_code', self.gf('django.db.models.fields.CharField')(default='55e3', max_length=4)),
            ('password', self.gf('django.db.models.fields.CharField')(default='0a609e7db7', max_length=10)),
        ))
        db.send_create_signal(u'notifier', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'Notification'
        db.delete_table(u'notifier_notification')


    models = {
        u'notifier.notification': {
            'Meta': {'object_name': 'Notification'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_token': ('django.db.models.fields.CharField', [], {'default': "'6056669d197848288619a45aab2125f6'", 'max_length': '32'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "'d6536f0e5c'", 'max_length': '10'}),
            'pruefungsplan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['notifier.Pruefungsplan']"}),
            'sms': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'default': "'958a'", 'max_length': '4'}),
            'sms_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'notifier.pruefungsplan': {
            'Meta': {'object_name': 'Pruefungsplan'},
            'available_since': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['notifier']