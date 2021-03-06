# Generated by Django 2.1.3 on 2019-01-30 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0023_auto_20190124_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionset',
            name='Number_of_questions',
        ),
        migrations.RemoveField(
            model_name='questionset',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='subscriptionpackage',
            name='scheduled_time_slot',
        ),
        migrations.AddField(
            model_name='audioquestion',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audios', to='question.Course'),
        ),
        migrations.AddField(
            model_name='passagequestion',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passages', to='question.Course'),
        ),
        migrations.AddField(
            model_name='questionset',
            name='number_of_audio_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionset',
            name='number_of_objective_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionset',
            name='number_of_passage_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionset',
            name='number_of_subjective_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionset',
            name='number_of_technical_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='questionset',
            name='scheduled_time_slot',
            field=models.ManyToManyField(related_name='question_sets', to='question.DateSlot'),
        ),
        migrations.RemoveField(
            model_name='subscriptionpackage',
            name='question_set',
        ),
        migrations.AddField(
            model_name='subscriptionpackage',
            name='question_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription_packages', to='question.QuestionSet'),
        ),
    ]
