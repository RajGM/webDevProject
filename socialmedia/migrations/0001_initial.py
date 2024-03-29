# Generated by Django 3.0.3 on 2023-03-17 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200)),
                ('follower', models.CharField(max_length=200)),
                ('chat_room', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postId', models.AutoField(primary_key=True, serialize=False)),
                ('postDate', models.DateField(null=True)),
                ('text', models.CharField(max_length=500)),
                ('likes', models.IntegerField(null=True)),
                ('media', models.ImageField(upload_to='dp')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='dp')),
                ('dateOfBirth', models.DateField(blank=True, null=True)),
                ('bio', models.CharField(blank=True, max_length=400, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
