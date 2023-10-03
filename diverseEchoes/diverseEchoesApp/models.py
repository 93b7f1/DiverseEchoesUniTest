from django.db import models
from django.contrib.auth.hashers import make_password
import hashlib
class UserProfile(models.Model):
    username = models.CharField(max_length=255)
    pixivuser = models.CharField(max_length=255, blank=True)
    spotify = models.CharField(max_length=255, blank=True)
    soundcloud = models.CharField(max_length=255, blank=True)
    youtube = models.CharField(max_length=255, blank=True)
    biografia = models.TextField(blank=True, default=' ')
    twitter = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self._state.adding or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['id']
        unique_together = ['username']

    def __str__(self):
        return self.username
class Echo(models.Model):
    echolink = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    genero = models.CharField(max_length=255)
    visualizacao = models.IntegerField()
    pixiv = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, related_name='echoes', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Echo"
        verbose_name_plural = "Echoes"
        ordering = ['id']

    def __str__(self):
        return self.echolink


class Comment(models.Model):
    comentario = models.CharField(max_length=255)
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1)
    data = models.CharField(max_length=255)
    echo = models.ForeignKey(Echo, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['id']

    def __str__(self):
        return self.comentario



