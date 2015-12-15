# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horserace', '0003_post_win_coef'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='result',
            field=models.SmallIntegerField(null=True),
        ),
    ]
