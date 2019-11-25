# Generated by Django 2.1.3 on 2019-01-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0013_auto_20190116_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('-----', '-----'), ('audio', 'Audio'), ('objective', 'Objective'), ('subjective', 'Subjective'), ('passage', 'Passage'), ('technical', 'Technical')], default='-----', max_length=10),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='question_type',
            field=models.CharField(choices=[('-----', '-----'), ('audio', 'Audio'), ('objective', 'Objective'), ('subjective', 'Subjective'), ('passage', 'Passage'), ('technical', 'Technical')], default='-----', max_length=10),
        ),
    ]
