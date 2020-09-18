from six import string_types
from django.contrib.auth.models import User
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from .models import Post


class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, string_types):
            value = value.split(',')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)
        return value


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = NewTagListSerializerField()

    class Meta:
        model = Post
        fields = ['slug',
                  'title',
                  'text',
                  'picture',
                  'author',
                  'tags',
                  'created_at',
                  'published_at',
                  'updated_at',
                  ]
        read_only_fields = ['slug',
                            'created_at',
                            'published_at',
                            'updated_at',
                            ]
