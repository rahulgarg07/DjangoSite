# Generated by Django 2.0.1 on 2018-03-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_post_info_post_publish_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post_info',
            name='post_video_url',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
