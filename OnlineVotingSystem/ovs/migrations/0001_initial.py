# Generated by Django 3.2.8 on 2021-12-15 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('description', models.CharField(default=' ', max_length=100)),
                ('city', models.CharField(default='', max_length=20)),
                ('phone', models.IntegerField(default=0)),
                ('head_shot', models.ImageField(blank=True, upload_to='profil_images')),
            ],
            options={
                'ordering': ['user'],
            },
        ),
    ]
