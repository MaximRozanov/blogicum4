from django.contrib import admin

from .models import Category, Comments, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at")
    actions = ["unpublish_comments"]

    def unpublish_comments(self, request, queryset):
        queryset.update(is_published=False)

    unpublish_comments.short_description = "Снять комментарии с публикации"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "category", "location", "author")
    list_editable = ("is_published",)
