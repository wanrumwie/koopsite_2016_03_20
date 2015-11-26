# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_list_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='list',
            field=models.TextField(null=True, default=''),
        ),
    ]
