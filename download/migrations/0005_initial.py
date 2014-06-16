# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Downloader'
        db.create_table(u'download_downloader', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('registration_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'download', ['Downloader'])


    def backwards(self, orm):
        # Deleting model 'Downloader'
        db.delete_table(u'download_downloader')


    models = {
        u'download.downloader': {
            'Meta': {'object_name': 'Downloader'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'registration_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['download']