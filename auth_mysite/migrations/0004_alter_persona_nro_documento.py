# Generated by Django 4.2.7 on 2024-10-07 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_mysite', '0003_alter_persona_celular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='nro_documento',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
