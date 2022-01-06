from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class Image(models.Model):
    image = models.ImageField(
        _("Image"), upload_to=upload_to, default='posts/default.jpg')

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.image.url


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, related_name="tags", on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')


    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    tag = models.ForeignKey(
        Tag, related_name='posts', on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=250)
    banner = models.URLField(null=True)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    status = models.CharField(
        max_length=10, choices=options, default='draft')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
