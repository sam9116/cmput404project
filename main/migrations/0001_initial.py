# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 04:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='author',
            fields=[
                ('profilepic', models.ImageField(blank=True, null=True, upload_to=b'upload', verbose_name=b'Images')),
                ('displayName', models.CharField(blank=True, editable=False, max_length=200, null=True)),
                ('host', models.CharField(blank=True, max_length=200, null=True)),
                ('url', models.URLField(blank=True, max_length=400, null=True)),
                ('github', models.URLField(blank=True, max_length=400, null=True)),
                ('bio', models.CharField(blank=True, max_length=1000, null=True)),
                ('authorid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('published', models.DateTimeField()),
                ('content', models.BinaryField(blank=True, max_length=10000, null=True)),
                ('commentid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contentType', models.CharField(choices=[(b'text/markdown', b'text/markdown'), (b'text/plain', b'text/plain'), (b'application/base64', b'application/base64'), (b'image/png;base64', b'image/png;base64'), (b'image/jpeg;base64', b'image/jpeg;base64')], default=b'text/plain', max_length=50)),
                ('authorid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.author')),
            ],
        ),
        migrations.CreateModel(
            name='friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorid1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='main.author')),
                ('authorid2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='main.author')),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('source', models.URLField(blank=True, max_length=400, null=True)),
                ('origin', models.URLField(blank=True, max_length=400, null=True)),
                ('description', models.CharField(max_length=1000)),
                ('contentType', models.CharField(choices=[(b'text/markdown', b'text/markdown'), (b'text/plain', b'text/plain'), (b'application/base64', b'application/base64'), (b'image/png;base64', b'image/png;base64'), (b'image/jpeg;base64', b'image/jpeg;base64')], default=b'text/plain', max_length=50)),
                ('content', models.BinaryField(blank=True, max_length=10000, null=True)),
                ('visibility', models.CharField(choices=[(b'PUBLIC', b'Public'), (b'FOAF', b'Friend of a Friend'), (b'FRIENDS', b'Friends only'), (b'PRIVATE', b'Private'), (b'SERVERONLY', b'Server Only')], default=b'FRIENDS', max_length=50)),
                ('published', models.DateTimeField()),
                ('postid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unlisted', models.BooleanField()),
                ('authorid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to='main.author')),
                ('categories', models.ManyToManyField(to='main.category')),
                ('comments', models.ManyToManyField(blank=True, to='main.comment')),
                ('visibleTo', models.ManyToManyField(blank=True, related_name='allowed_author', to='main.author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='postid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.post'),
        ),
    ]
