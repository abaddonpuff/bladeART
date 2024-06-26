# Generated by Django 4.1.2 on 2024-04-26 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='breachStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('handle', models.CharField(max_length=100, unique=True)),
                ('userId', models.BigIntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
