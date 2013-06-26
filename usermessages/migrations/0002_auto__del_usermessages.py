# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserMessages'
        db.delete_table('usermessages_usermessages')


    def backwards(self, orm):
        # Adding model 'UserMessages'
        db.create_table('usermessages_usermessages', (
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_messages', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(related_name='received_messages', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('usermessages', ['UserMessages'])


    models = {
        
    }

    complete_apps = ['usermessages']