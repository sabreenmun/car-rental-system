# Generated by Django 5.1.6 on 2025-03-12 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_remove_message_is_read_remove_message_receiver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
