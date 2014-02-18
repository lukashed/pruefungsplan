# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Pruefungsplan.available_since'
        db.alter_column(u'notifier_pruefungsplan', 'available_since', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Pruefungsplan.available_since'
        raise RuntimeError("Cannot reverse this migration. 'Pruefungsplan.available_since' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Pruefungsplan.available_since'
        db.alter_column(u'notifier_pruefungsplan', 'available_since', self.gf('django.db.models.fields.DateTimeField')())

    models = {
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