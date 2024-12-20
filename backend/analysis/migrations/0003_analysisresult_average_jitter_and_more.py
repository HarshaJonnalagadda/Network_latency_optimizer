# Generated by Django 5.1.4 on 2024-12-18 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_alter_analysisresult_optimizations'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisresult',
            name='average_jitter',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='analysisresult',
            name='average_packet_loss',
            field=models.FloatField(default=0.0),
        ),
    ]
