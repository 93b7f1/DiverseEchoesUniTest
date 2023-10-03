from django.contrib import admin

from .models import Comment, Echo, UserProfile


@admin.register(Echo)
class EchoAdmin(admin.ModelAdmin):
    list_display = ('echolink','genero','visualizacao','url')


@admin.register(Comment)
class UserAdmin(admin.ModelAdmin):
    list_display = ('comentario', 'avaliacao', 'data')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','email','pixivuser')