# Generated by Django 2.1.3 on 2019-01-17 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0015_question_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioquestion',
            name='marks_per_question',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='passagequestion',
            name='no_of_questions',
            field=models.IntegerField(default=5),
        ),
    ]
