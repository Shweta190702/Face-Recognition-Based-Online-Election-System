# Generated by Django 3.2.9 on 2022-02-25 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ovs', '0010_alter_vote_party_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='vid',
            field=models.CharField(default='', max_length=11),
        ),
    ]