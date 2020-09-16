# Generated by Django 3.1.1 on 2020-09-15 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Изображение')),
                ('title', models.CharField(max_length=128, null=True, verbose_name='Заголовок')),
                ('text', tinymce.models.HTMLField(null=True, verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('published_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('slug', models.SlugField(default='', editable=False, max_length=256)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['published_at'],
            },
        ),
    ]
