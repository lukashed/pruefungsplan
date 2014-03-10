# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Exam'
        db.create_table(u'notifier_exam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pruefungsplan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exams', to=orm['notifier.Pruefungsplan'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'notifier', ['Exam'])


    def backwards(self, orm):
        # Deleting model 'Exam'
        db.delete_table(u'notifier_exam')


    models = {
        u'notifier.exam': {
            'Meta': {'object_name': 'Exam'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pruefungsplan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exams'", 'to': u"orm['notifier.Pruefungsplan']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'notifier.notification': {
            'Meta': {'object_name': 'Notification'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email_token': ('django.db.models.fields.CharField', [], {'default': "'c4f80921b2484429b98b130c5705a1cf'", 'max_length': '32'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "'41ace59f8e'", 'max_length': '10'}),
            'pruefungsplan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': u"orm['notifier.Pruefungsplan']"}),
            'sms': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'default': "'59d5'", 'max_length': '4'}),
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