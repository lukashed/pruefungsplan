# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field exams on 'Notification'
        m2m_table_name = db.shorten_name(u'notifier_notification_exams')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('notification', models.ForeignKey(orm[u'notifier.notification'], null=False)),
            ('exam', models.ForeignKey(orm[u'notifier.exam'], null=False))
        ))
        db.create_unique(m2m_table_name, ['notification_id', 'exam_id'])


        # Changing field 'Notification.pruefungsplan'
        db.alter_column(u'notifier_notification', 'pruefungsplan_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['notifier.Pruefungsplan']))

    def backwards(self, orm):
        # Removing M2M table for field exams on 'Notification'
        db.delete_table(db.shorten_name(u'notifier_notification_exams'))


        # User chose to not deal with backwards NULL issues for 'Notification.pruefungsplan'
        raise RuntimeError("Cannot reverse this migration. 'Notification.pruefungsplan' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Notification.pruefungsplan'
        db.alter_column(u'notifier_notification', 'pruefungsplan_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifier.Pruefungsplan']))

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
            'email_token': ('django.db.models.fields.CharField', [], {'default': "'3acaf24120144a3abcda45f96129466e'", 'max_length': '32'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exams': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'notifications'", 'blank': 'True', 'to': u"orm['notifier.Exam']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "'38c9c12d3a'", 'max_length': '10'}),
            'pruefungsplan': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notifications'", 'null': 'True', 'to': u"orm['notifier.Pruefungsplan']"}),
            'sms': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'sms_code': ('django.db.models.fields.CharField', [], {'default': "'daee'", 'max_length': '4'}),
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