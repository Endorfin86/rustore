# Generated by Django 4.1.3 on 2022-11-30 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='time',
            field=models.CharField(default='30-11-2022 18:46', max_length=100, verbose_name='Время'),
        ),
    ]
