from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('slug',
    #                     'title',
    #                     'author',
    #                     'tags',
    #                     'published_at',
    #                     )
