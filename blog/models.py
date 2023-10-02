
from django.db import models

from config import settings
from users.models import User

NULL_BLANK = {'null': True, 'blank': True}


DRAFT = 'DRAFT'
PUBLISHED = 'PUBLISHED'

STATUS_CHOICES = (
    (DRAFT, 'Draft'),
    (PUBLISHED, 'Published'),
)


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title', unique=True, )
    slug = models.SlugField(max_length=100, verbose_name='Slug', **NULL_BLANK, unique=True, )
    content = models.TextField(verbose_name='Content', **NULL_BLANK, )
    image = models.ImageField(upload_to='blog/', verbose_name='Image Preview', **NULL_BLANK, )
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date Created', )
    date_uploaded = models.DateTimeField(auto_now=True, verbose_name='Date Uploaded', )

    views_count = models.IntegerField(default=0, verbose_name='Views Count', )
    is_published = models.BooleanField(default=True, verbose_name='Is Published',)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'
        ordering = ['-date_created']



