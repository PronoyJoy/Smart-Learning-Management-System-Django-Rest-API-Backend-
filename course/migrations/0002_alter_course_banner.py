# Generated by Django 5.2.3 on 2025-07-15 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='course_banners/'),
        ),
    ]
