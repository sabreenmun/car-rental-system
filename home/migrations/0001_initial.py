# Generated by Django 5.1.7 on 2025-03-28 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('security_question_1', models.CharField(max_length=255)),
                ('security_answer_1', models.CharField(max_length=255)),
                ('security_question_2', models.CharField(max_length=255)),
                ('security_answer_2', models.CharField(max_length=255)),
                ('security_question_3', models.CharField(max_length=255)),
                ('security_answer_3', models.CharField(max_length=255)),
            ],
        ),
    ]
