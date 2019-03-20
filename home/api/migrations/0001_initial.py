# Generated by Django 2.1.7 on 2019-03-16 13:33

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Furnace',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status',
                 model_utils.fields.StatusField(
                     choices=[('OFF', 'OFF'), ('FAN', 'FAN'), ('HEAT', 'HEAT')],
                     default='OFF',
                     max_length=100,
                     no_check_for_status=True)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address',
                 models.CharField(
                     help_text=
                     'For info purposes only. '
                     'Maybe useful in a cloud db where all houses are stored',
                     max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='lights', max_length=30)),
                ('slug',
                 autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('status',
                 model_utils.fields.StatusField(
                     choices=[('ON', 'ON'), ('OFF', 'OFF')],
                     default='OFF',
                     max_length=100,
                     no_check_for_status=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('slug',
                 autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('house',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.House')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('slug',
                 autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('room',
                 models.ForeignKey(
                     null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Room')),
            ],
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('sensor',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sensor')),
            ],
            options={
                'db_table': 'api_sensor_data',
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('slug',
                 autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True)),
                ('display_symbol', models.CharField(help_text='Unit of measure', max_length=5)),
            ],
            options={
                'db_table': 'api_sensor_type',
            },
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='api.SensorType'),
        ),
        migrations.AddField(
            model_name='light',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Room'),
        ),
        migrations.AddField(
            model_name='furnace',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.House'),
        ),
    ]
