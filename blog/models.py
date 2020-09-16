import datetime
import itertools

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from googletrans import Translator
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from tinymce.models import HTMLField


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', null=True, on_delete=models.SET_NULL)
    picture = models.ImageField('Изображение',
                                upload_to='posts/',
                                null=True,
                                blank=True
                                )
    title = models.CharField('Заголовок', max_length=128, null=True)
    text = HTMLField('Текст', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    published_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(default='',
                            editable=False,
                            max_length=256,
                            )

    tags = TaggableManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['published_at']

    def __str__(self):
        return self.title

    def _generate_slug(self):
        value = Translator().translate('{}'.format(self.title), dest='en').text
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Post.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)

    def was_published(self):
        return self.published_at <= timezone.now()

    def was_published_recently(self):
        return self.published_at >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'published_at'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Было ли создано недавно?'
