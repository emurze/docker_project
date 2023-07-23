from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('DR', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64, unique_for_date='publish')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.PUBLISHED)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        publish = self.publish
        return reverse('base:detail', args=[publish.year, publish.month,
                                            publish.day, self.slug])

    def get_absolute_url_for_share(self):
        return reverse('base:share', args=[self.pk])

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=('-publish',))
        ]

    def __str__(self) -> str:
        return self.title  # type: ignore


class CommentObjects(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('post')


class Comment(models.Model):
    post = models.ForeignKey(Post,  related_query_name='comment',
                             on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, related_query_name='comment',
                             on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    updated = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                               related_name='replies')

    objects = models.Manager()
    co_objects = CommentObjects()

    class Meta:
        ordering = ('-updated',)
        indexes = [
            models.Index(fields=('-updated',))
        ]

    def __str__(self):
        return '<comment - %s of post - %s>' % (self.pk, self.post)
