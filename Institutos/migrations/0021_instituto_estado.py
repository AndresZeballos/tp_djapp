# Generated by Django 2.0.3 on 2018-11-24 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institutos', '0020_calle_omnibus_parada'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituto',
            name='estado',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
