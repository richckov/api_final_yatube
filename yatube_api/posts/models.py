from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=200, unique=True,)
    description = models.TextField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group, models.SET_NULL,
        blank=True, null=True, related_name='posts',
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        UniqueConstraint(fields=['user', 'following'], name='unique_follow')
        CheckConstraint(
            check=~Q(user=F('following')),
            name='not_follow_yourselfe'
        )
