# Generated by Django 5.0.2 on 2024-02-14 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('types', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Instagram', 'Instagram'), ('Facebook', 'Facebook')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usertoken', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
