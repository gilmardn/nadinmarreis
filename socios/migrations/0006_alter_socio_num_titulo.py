# Generated by Django 5.1.3 on 2025-01-20 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0005_alter_socio_endereco_alter_socio_num_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socio',
            name='num_titulo',
            field=models.CharField(blank=True, default='000', max_length=3, null=True, verbose_name='Numero Titulo'),
        ),
    ]
