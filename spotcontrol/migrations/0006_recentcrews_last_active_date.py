# Generated by Django 3.0.5 on 2020-04-15 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotcontrol', '0005_auto_20200415_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='recentcrews',
            name='last_active_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
