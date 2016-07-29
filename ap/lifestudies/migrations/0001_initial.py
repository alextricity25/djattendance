# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infraction', models.CharField(max_length=4, choices=[(b'AT', b'Attendance'), (b'CI', b'Cell Phone & Internet'), (b'MS', b'Missed Service'), (b'S', b'Speeding'), (b'AN', b'Alarm Noise'), (b'G', b'Guard'), (b'C', b'Curfew'), (b'M', b'Misplaced Item'), (b'HI', b'House Inspection'), (b'L', b'Library'), (b'MISC', b'Misc')])),
                ('quantity', models.PositiveSmallIntegerField()),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('due', models.DateTimeField()),
                ('offense', models.CharField(default=b'RO', max_length=2, choices=[(b'MO', b'Monday Offense'), (b'RO', b'Regular Offense')])),
                ('note', models.TextField(blank=True)),
                ('trainee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['trainee__lastname'],
            },
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('chapter', models.PositiveSmallIntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('fellowship', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('minimum_words', models.PositiveSmallIntegerField(default=250)),
                ('hard_copy', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='books.Book')),
                ('discipline', models.ForeignKey(to='lifestudies.Discipline')),
            ],
            options={
                'ordering': ['approved'],
            },
        ),
    ]
