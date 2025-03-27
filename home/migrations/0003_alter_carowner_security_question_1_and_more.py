# Generated by Django 5.1.6 on 2025-03-09 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_carowner_security_question_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carowner',
            name='security_question_1',
            field=models.CharField(choices=[('first_pet', 'What was the name of your first pet?'), ('mother_maiden', 'What is your mother’s maiden name?'), ('first_car', 'What was the model of your first car?')], max_length=50),
        ),
        migrations.AlterField(
            model_name='carowner',
            name='security_question_2',
            field=models.CharField(choices=[('first_pet', 'What was the name of your first pet?'), ('mother_maiden', 'What is your mother’s maiden name?'), ('first_car', 'What was the model of your first car?')], max_length=50),
        ),
        migrations.AlterField(
            model_name='carowner',
            name='security_question_3',
            field=models.CharField(choices=[('first_pet', 'What was the name of your first pet?'), ('mother_maiden', 'What is your mother’s maiden name?'), ('first_car', 'What was the model of your first car?')], max_length=50),
        ),
    ]
