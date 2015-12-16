# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='timestamp',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='resume',
            name='latest_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
