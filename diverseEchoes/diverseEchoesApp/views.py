from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Echo, Comment, UserProfile
from .serializers import EchoSerializer, ComentarioSerializer, UserProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from django.contrib.auth.hashers import check_password

from django.http import JsonResponse
from .models import UserProfile
"""
API V1
"""
class EchoesAPIView(generics.ListCreateAPIView):
    queryset = Echo.objects.all()
    serializer_class = EchoSerializer


    def get_queryset(self):
        if self.kwargs.get('comment_pk'):
            return self.queryset.filter(comment_pk = self.kwargs.get('comment_pk'))
        return self.queryset.all()



class CommentsAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = ComentarioSerializer



class EchoAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Echo.objects.all()
    serializer_class = EchoSerializer

    def get_object(self):
        if self.kwargs.get('comment_pk'):
            return get_object_or_404(self.get_queryset(),
                                     comment_id=self.kwargs.get('comment_pk'),
                                     pk=self.kwargs.get('echo_pk'))
        return get_object_or_404(self.get_queryset(),pk=self.kwargs.get('echo_pk'))





class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user_profile = UserProfile.objects.get(username=username)

            if check_password(password, user_profile.password):
                return JsonResponse({'message': 'Login bem-sucedido'})
            else:
                return JsonResponse({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)


"""
API V2
"""
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ComentarioSerializer

    @action(detail=True,methods=['get'])
    def echoes(self,request,pk=None):
        user = self.get_object()
        serializer = EchoSerializer(user.echoes.all(), many=True)
        return Response(serializer.data)


class EchoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Echo.objects.all()
    serializer_class = EchoSerializer

class CommentViewSetM(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = ComentarioSerializer


class UserProfileViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class EchoViewSetLastFive(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Echo.objects.all()
    serializer_class = EchoSerializer

    @action(detail=False, methods=['GET'])
    def last(self, request):
        last_5_echoes = self.queryset.order_by('-id')[:5].values_list('id', flat=True)
        return Response(last_5_echoes, status=status.HTTP_200_OK)


class EchoCommentsViewSet(viewsets.ModelViewSet):
    serializer_class = ComentarioSerializer
    def get_queryset(self):
        echo_id = self.kwargs.get('echo_id')
        echo = Echo.objects.get(pk=echo_id)
        comments = Comment.objects.filter(echo=echo)[:3]
        return comments