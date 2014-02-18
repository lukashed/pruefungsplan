# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Pruefungsplan'
        db.create_table(u'notifier_pruefungsplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_since', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'notifier', ['Pruefungsplan'])


    def backwards(self, orm):
        # Deleting model 'Pruefungsplan'
        db.delete_table(u'notifier_pruefungsplan')


    models = {
        u'notifier.pruefungsplan': {
            'Meta': {'object_name': 'Pruefungsplan'},
            'available_since': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['notifier']