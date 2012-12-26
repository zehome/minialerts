# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlertMatch'
        db.create_table('alerts_alertmatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('regex', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('emails', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('alerts', ['AlertMatch'])

        # Adding model 'Alert'
        db.create_table('alerts_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('atype', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('arange', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('ipaddr', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('extinfo', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_tick', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('date_last_alerted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('checked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('alerts', ['Alert'])


    def backwards(self, orm):
        # Deleting model 'AlertMatch'
        db.delete_table('alerts_alertmatch')

        # Deleting model 'Alert'
        db.delete_table('alerts_alert')


    models = {
        'alerts.alert': {
            'Meta': {'object_name': 'Alert'},
            'arange': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'atype': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'checked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_alerted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_last_tick': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'extinfo': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'alerts.alertmatch': {
            'Meta': {'object_name': 'AlertMatch'},
            'emails': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['alerts']