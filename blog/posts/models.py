from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    categories = models.ManyToManyField('Category', through='PostCategories')

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
