# Generated by Django 3.0.5 on 2020-04-15 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotcontrol', '0006_recentcrews_last_active_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recentcrews',
            options={'ordering': ['last_active_date']},
        ),
    ]