from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('publish', )
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    search_fields = ('title', 'content')
    date_hierarchy = 'publish'
    ordering = ('-publish', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('updated', )
    raw_id_fields = ('post', 'user')
    search_fields = ('content', 'post', 'user')
    ordering = ('-updated',)
