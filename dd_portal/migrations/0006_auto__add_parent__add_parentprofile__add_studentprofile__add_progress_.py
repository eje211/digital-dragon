# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Parent'
        db.create_table(u'dd_portal_parent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('parentprofile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dd_portal.ParentProfile'], unique=True, null=True)),
        ))
        db.send_create_signal(u'dd_portal', ['Parent'])

        # Adding M2M table for field groups on 'Parent'
        m2m_table_name = db.shorten_name(u'dd_portal_parent_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm[u'dd_portal.parent'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parent_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Parent'
        m2m_table_name = db.shorten_name(u'dd_portal_parent_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('parent', models.ForeignKey(orm[u'dd_portal.parent'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['parent_id', 'permission_id'])

        # Adding model 'ParentProfile'
        db.create_table(u'dd_portal_parentprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ice_contact', self.gf('django.db.models.fields.CharField')(default='<MISSING>', max_length=255)),
            ('notes', self.gf('tinymce.models.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'dd_portal', ['ParentProfile'])

        # Adding model 'StudentProfile'
        db.create_table(u'dd_portal_studentprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school_grade', self.gf('django.db.models.fields.CharField')(default='active', max_length=2)),
        ))
        db.send_create_signal(u'dd_portal', ['StudentProfile'])

        # Adding model 'Progress'
        db.create_table(u'dd_portal_progress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.StudentProfile'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.Course'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='05', max_length=16)),
        ))
        db.send_create_signal(u'dd_portal', ['Progress'])

        # Adding model 'Student'
        db.create_table(u'dd_portal_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dd_portal.StudentProfile'], unique=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.Parent'], null=True)),
        ))
        db.send_create_signal(u'dd_portal', ['Student'])

        # Adding M2M table for field groups on 'Student'
        m2m_table_name = db.shorten_name(u'dd_portal_student_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'dd_portal.student'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Student'
        m2m_table_name = db.shorten_name(u'dd_portal_student_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'dd_portal.student'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'permission_id'])


    def backwards(self, orm):
        # Deleting model 'Parent'
        db.delete_table(u'dd_portal_parent')

        # Removing M2M table for field groups on 'Parent'
        db.delete_table(db.shorten_name(u'dd_portal_parent_groups'))

        # Removing M2M table for field user_permissions on 'Parent'
        db.delete_table(db.shorten_name(u'dd_portal_parent_user_permissions'))

        # Deleting model 'ParentProfile'
        db.delete_table(u'dd_portal_parentprofile')

        # Deleting model 'StudentProfile'
        db.delete_table(u'dd_portal_studentprofile')

        # Deleting model 'Progress'
        db.delete_table(u'dd_portal_progress')

        # Deleting model 'Student'
        db.delete_table(u'dd_portal_student')

        # Removing M2M table for field groups on 'Student'
        db.delete_table(db.shorten_name(u'dd_portal_student_groups'))

        # Removing M2M table for field user_permissions on 'Student'
        db.delete_table(db.shorten_name(u'dd_portal_student_user_permissions'))


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
        u'dd_portal.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'dd_portal.parent': {
            'Meta': {'object_name': 'Parent'},
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
            'parentprofile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dd_portal.ParentProfile']", 'unique': 'True', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'dd_portal.parentprofile': {
            'Meta': {'object_name': 'ParentProfile'},
            'ice_contact': ('django.db.models.fields.CharField', [], {'default': "'<MISSING>'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('tinymce.models.HTMLField', [], {'blank': 'True'})
        },
        u'dd_portal.progress': {
            'Meta': {'object_name': 'Progress'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dd_portal.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'05'", 'max_length': '16'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dd_portal.StudentProfile']"})
        },
        u'dd_portal.student': {
            'Meta': {'object_name': 'Student'},
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
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dd_portal.Parent']", 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dd_portal.StudentProfile']", 'unique': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'dd_portal.studentprofile': {
            'Meta': {'object_name': 'StudentProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_grade': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '2'})
        }
    }

    complete_apps = ['dd_portal']