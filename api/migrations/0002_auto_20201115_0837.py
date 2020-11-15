# Generated by Django 3.1.2 on 2020-11-15 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HereData',
            fields=[
                ('link_dir', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('tx', models.DateTimeField()),
                ('length', models.IntegerField(blank=True, null=True)),
                ('mean', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('stddev', models.DecimalField(blank=True, decimal_places=65535, max_digits=65535, null=True)),
                ('confidence', models.IntegerField(blank=True, null=True)),
                ('pct_85', models.IntegerField(blank=True, null=True)),
                ('pct_95', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'here_data',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='TravelTime',
        ),
    ]
