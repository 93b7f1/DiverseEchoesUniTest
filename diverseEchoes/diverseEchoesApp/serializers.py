from rest_framework import serializers
from .models import Echo, Comment, UserProfile


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'comentario',
            'avaliacao',
            'data',
            'echo',
        )


class EchoSerializer(serializers.ModelSerializer):
    comments = ComentarioSerializer(many=True, read_only=True)

    class Meta:
        model = Echo
        fields = (
            'id',
            'echolink',
            'url',
            'genero',
            'visualizacao',
            'pixiv',
            'tipo',
            'comments',
            'user',
        )

class UserProfileSerializer(serializers.ModelSerializer):

    echoes = EchoSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'username',
            'pixivuser',
            'biografia',
            'twitter',
            'spotify',
            'soundcloud',
            'youtube',
            'password',
            'email',
            'echoes',
        )
