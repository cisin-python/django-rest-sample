# Generated by Django 2.1.3 on 2019-01-21 11:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0020_auto_20190119_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionset',
            name='scheduled_time_slot',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
