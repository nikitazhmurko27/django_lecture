from django.contrib import admin
from .models import Post
from .models import Category


class PostCategoriesInline(admin.TabularInline):
    model = Post.categories.through


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [
        PostCategoriesInline
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
