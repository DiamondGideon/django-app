# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horserace', '0002_auto_20151212_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='win_coef',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
