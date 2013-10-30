# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'StudentProfile.parent'
        db.alter_column(u'dragon_portal_studentprofile', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['dragon_portal.ParentProfile']))

    def backwards(self, orm):

        # Changing field 'StudentProfile.parent'
        db.alter_column(u'dragon_portal_studentprofile', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dragon_portal.ParentProfile'], null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dragon_portal.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'dragon_portal.dragonuser': {
            'Meta': {'object_name': 'DragonUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'parent_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dragon_portal.ParentProfile']", 'unique': 'True', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'student_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dragon_portal.StudentProfile']", 'unique': 'True', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "'admin'", 'max_length': '16'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'dragon_portal.parentprofile': {
            'Meta': {'object_name': 'ParentProfile'},
            'ice_contact': ('django.db.models.fields.CharField', [], {'default': "'<MISSING>'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('tinymce.models.HTMLField', [], {'blank': 'True'})
        },
        u'dragon_portal.progress': {
            'Meta': {'object_name': 'Progress'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dragon_portal.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'05'", 'max_length': '16'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dragon_portal.StudentProfile']"})
        },
        u'dragon_portal.studentprofile': {
            'Meta': {'object_name': 'StudentProfile'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dragon_portal.Course']", 'through': u"orm['dragon_portal.Progress']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dragon_portal.ParentProfile']"}),
            'school_grade': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '2'})
        }
    }

    complete_apps = ['dragon_portal']