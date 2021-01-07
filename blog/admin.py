from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    list_filter = ('status', 'created_at', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'body')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
