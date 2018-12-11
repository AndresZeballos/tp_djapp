# Generated by Django 2.1.3 on 2018-12-11 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institutos', '0027_auto_20181211_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituto',
            name='descripcion',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='descripcion_corta',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='direccion',
            field=models.CharField(default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='instituto',
            name='subtitulo',
            field=models.CharField(default='', max_length=500),
        ),
    ]
