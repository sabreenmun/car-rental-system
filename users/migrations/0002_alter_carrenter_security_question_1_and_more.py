# Generated by Django 5.1.7 on 2025-03-26 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrenter',
            name='security_question_1',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='carrenter',
            name='security_question_2',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='carrenter',
            name='security_question_3',
            field=models.CharField(max_length=255),
        ),
    ]
