from django.contrib import admin

from webapp.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'text']
    fields = ['title', 'author', 'text', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


# Register your models here.
admin.site.register(Article, ArticleAdmin)