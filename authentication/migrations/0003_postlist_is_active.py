# Generated by Django 5.0.2 on 2024-02-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_list_postlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
