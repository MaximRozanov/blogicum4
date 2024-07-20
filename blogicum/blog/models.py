from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_LENGTH

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH)
    description = models.TextField("Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text="Идентификатор страницы для URL;"
        " разрешены символы латиницы, цифры, дефис и подчёркивание.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField("Название места", max_length=MAX_LENGTH)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        "можно делать отложенные публикации.",
    )
    image = models.ImageField("Фото", upload_to="post_photo", blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title


class Comments(models.Model):
    text = models.TextField("text")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return self.title
