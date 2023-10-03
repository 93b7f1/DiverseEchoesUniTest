from django.urls import path

from .views import (EchoAPIView, CommentsAPIView, EchoesAPIView, EchoViewSet, CommentViewSet, EchoViewSetLastFive, EchoCommentsViewSet
,UserProfileViewSet, CommentViewSetM,CustomLoginView)

from rest_framework.routers import SimpleRouter
# Endpoints na V2
router = SimpleRouter()
router.register('echo', EchoViewSet)
router.register('comment', CommentViewSet)
router.register('echo-last', EchoViewSetLastFive)
router.register('user', UserProfileViewSet)
router.register('commentM', CommentViewSetM)


urlpatterns = [
    # Lista Echos na V1
    path('echoes/', EchoesAPIView.as_view(), name='echoes'),

    # Lista top 3 comentarios de um echo na V1
    path('top3-comments/<int:echo_id>/', EchoCommentsViewSet.as_view({'get': 'list'}), name='top3-comments'),

    # Apenas 1 echo pelo id na V1
    path('echo/<int:echo_pk>/', EchoAPIView.as_view(), name='echo'),

    # Lista todos os comentarios de todos os echoes na v1
    path('comments/', CommentsAPIView.as_view(), name='comments'),

    path('login/', CustomLoginView.as_view(), name='login'),


]
