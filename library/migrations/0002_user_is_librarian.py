# Generated by Django 5.1 on 2024-12-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_librarian',
            field=models.BooleanField(default=False),
        ),
    ]
