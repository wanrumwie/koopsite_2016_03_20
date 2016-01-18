# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20151126_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(to='lists.List', default=None),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(unique=True, default=''),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('list', 'text')]),
        ),
    ]
