# Generated by Django 2.0.5 on 2018-06-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institutos', '0005_usuariolegado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariolegado',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usuariolegado',
            name='password',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
