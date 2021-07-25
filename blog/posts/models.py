from tags.models import TaggedItem
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Post.STATUS_PUBLISH)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()


class Post(models.Model):
    objects = PostManager()
    STATUS_DRAFT = 'D'
    STATUS_PUBLISH = 'P'
    STATUS_REJECTED = 'R'
    STATUS = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISH, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
    )
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    categories = models.ManyToManyField('Category', through='PostCategories')
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS_DRAFT)
    tags = GenericRelation(TaggedItem)

    def get_absolute_url(self):
        return reverse("posts:index")

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PostCategories(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)
