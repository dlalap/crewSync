# Generated by Django 2.2.1 on 2020-03-10 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotcontrol', '0002_spotifyuser_expires_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuser',
            name='auth_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
