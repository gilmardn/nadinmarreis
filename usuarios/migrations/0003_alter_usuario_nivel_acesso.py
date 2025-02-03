# Generated by Django 5.1.3 on 2025-02-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_usuario_nivel_acesso'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nivel_acesso',
            field=models.CharField(choices=[('admin', 'Administrador'), ('financeiro', 'Financeiro'), ('social', 'Social'), ('esportivo', 'Esportivo'), ('basico', 'Basico')], default='basico', max_length=20),
        ),
    ]
