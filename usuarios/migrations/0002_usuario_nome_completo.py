# Generated by Django 5.1.3 on 2025-01-01 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='nome_completo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
