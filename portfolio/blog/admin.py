# admin.py
from django.contrib import admin
from .models import Posts
from unfold.admin import ModelAdmin 

@admin.register(Posts)
class PostsAdmin(ModelAdmin):
    list_display = ('post_title', 'post_date', 'update_date', 'views', 'likes')
    prepopulated_fields = {'slug': ('post_title',)}  # Auto-fill slug from title

# OR simply:
# admin.site.register(Posts)
