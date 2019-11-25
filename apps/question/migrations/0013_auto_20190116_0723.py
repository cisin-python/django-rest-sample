# Generated by Django 2.1.3 on 2019-01-16 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0012_auto_20190116_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioquestion',
            name='no_of_questions',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='scheduled_time_slot',
            field=models.ManyToManyField(related_name='question_sets', to='question.DateSlot'),
        ),
    ]