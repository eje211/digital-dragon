# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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


    def backwards(self, orm):
        # Adding model 'Parent'
        db.create_table(u'dd_portal_parent', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('parentprofile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dd_portal.ParentProfile'], unique=True, null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
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
            ('notes', self.gf('tinymce.models.HTMLField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ice_contact', self.gf('django.db.models.fields.CharField')(default='<MISSING>', max_length=255)),
        ))
        db.send_create_signal(u'dd_portal', ['ParentProfile'])

        # Adding model 'StudentProfile'
        db.create_table(u'dd_portal_studentprofile', (
            ('school_grade', self.gf('django.db.models.fields.CharField')(default='active', max_length=2)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'dd_portal', ['StudentProfile'])

        # Adding model 'Progress'
        db.create_table(u'dd_portal_progress', (
            ('status', self.gf('django.db.models.fields.CharField')(default='05', max_length=16)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.Course'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.StudentProfile'])),
        ))
        db.send_create_signal(u'dd_portal', ['Progress'])

        # Adding model 'Student'
        db.create_table(u'dd_portal_student', (
            ('profile', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['dd_portal.StudentProfile'], unique=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dd_portal.Parent'], null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
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


    models = {
        u'dd_portal.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('tinymce.models.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['dd_portal']