# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Incentive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('schemeID', models.IntegerField(default=0)),
                ('schemeName', models.CharField(default=b'', max_length=100, blank=True)),
                ('typeID', models.IntegerField(default=0)),
                ('typeName', models.CharField(default=b'', max_length=100, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('ordinal', models.IntegerField(default=0, null=True, blank=True)),
                ('modeID', models.IntegerField(default=0)),
                ('presentationDuration', models.DateTimeField(auto_now_add=True)),
                ('groupIncentive', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('condition', models.TextField()),
                ('owner', models.ForeignKey(related_name='incentive', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=120, null=True, blank=True)),
                ('last_name', models.CharField(max_length=120, null=True, blank=True)),
                ('email', models.EmailField(max_length=75)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagID', models.IntegerField()),
                ('tagName', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='incentive',
            name='tags',
            field=models.ManyToManyField(to='signups.Tag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
