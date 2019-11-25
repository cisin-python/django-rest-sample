# Generated by Django 2.1.3 on 2019-01-14 06:01

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_auto_20190102_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audiofile')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PassageQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('question_text', ckeditor.fields.RichTextField()),
                ('marks_per_question', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='questionset',
            name='Number_of_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='audio_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audio_questions', to='question.AudioQuestion'),
        ),
        migrations.AddField(
            model_name='question',
            name='passage_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passage_questions', to='question.PassageQuestion'),
        ),
    ]