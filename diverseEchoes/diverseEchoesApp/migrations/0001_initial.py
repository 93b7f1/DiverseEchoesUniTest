# Generated by Django 4.0.10 on 2023-10-02 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('pixivuser', models.CharField(blank=True, max_length=255)),
                ('spotify', models.CharField(blank=True, max_length=255)),
                ('soundcloud', models.CharField(blank=True, max_length=255)),
                ('youtube', models.CharField(blank=True, max_length=255)),
                ('biografia', models.TextField(blank=True, default=' ')),
                ('twitter', models.CharField(blank=True, max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['id'],
                'unique_together': {('username',)},
            },
        ),
        migrations.CreateModel(
            name='Echo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('echolink', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('genero', models.CharField(max_length=255)),
                ('visualizacao', models.IntegerField()),
                ('pixiv', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='echoes', to='diverseEchoesApp.userprofile')),
            ],
            options={
                'verbose_name': 'Echo',
                'verbose_name_plural': 'Echoes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=255)),
                ('avaliacao', models.DecimalField(decimal_places=1, max_digits=2)),
                ('data', models.CharField(max_length=255)),
                ('echo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='diverseEchoesApp.echo')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['id'],
            },
        ),
    ]