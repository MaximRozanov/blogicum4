from django.contrib import admin

from blog.models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "created_at")
    actions = ["unpublish_comments"]

    @admin.display(
        description="Снять комментарии с публикации",
    )
    def unpublish_comments(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "category", "location", "author")
    list_editable = ("is_published",)
