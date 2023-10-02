from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'date_created')
    search_fields = ('title', 'content', 'date_created',)
    list_filter = ('title', 'content', 'date_created',)
