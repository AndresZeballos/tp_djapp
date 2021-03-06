# Generated by Django 2.0.3 on 2018-04-17 00:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Centro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Comodidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Facilidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instituto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('barrios', models.ManyToManyField(to='Institutos.Barrio')),
                ('centros', models.ManyToManyField(to='Institutos.Centro')),
                ('comodidades', models.ManyToManyField(to='Institutos.Comodidad')),
                ('facilidades', models.ManyToManyField(to='Institutos.Facilidad')),
                ('formasPago', models.ManyToManyField(to='Institutos.FormaPago')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Institutos.Centro')),
            ],
        ),
        migrations.CreateModel(
            name='Mensajes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('nombre', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('mensaje', models.CharField(max_length=4000)),
                ('centro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Institutos.Centro')),
                ('instituto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='Institutos.Instituto')),
            ],
        ),
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('instituto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Institutos.Instituto')),
            ],
        ),
        migrations.CreateModel(
            name='RedSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distancia', models.IntegerField(default=0)),
                ('lineas', models.CharField(max_length=200)),
                ('instituto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Institutos.Instituto')),
            ],
        ),
        migrations.AddField(
            model_name='mensajes',
            name='motivo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Institutos.Motivo'),
        ),
        migrations.AddField(
            model_name='enlace',
            name='instituto',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Institutos.Instituto'),
        ),
        migrations.AddField(
            model_name='enlace',
            name='redSocial',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='Institutos.RedSocial'),
        )
    ]
