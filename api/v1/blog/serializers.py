from django.utils import timezone
from rest_framework import serializers
from taggit.models import Tag
from blog.models import Post, Comment, Category, ActionSummary, Like
from django.contrib.auth.models import User


# https://stackoverflow.com/questions/17331578/django-rest-framework-timezone-aware-renderers-parsers
class DateTimeTzAwareField(serializers.DateTimeField):
    def to_representation(self, value):
        if value:
            value = timezone.localtime(value)
        return super(DateTimeTzAwareField, self).to_representation(value)


# Define serializer for comment in post
class UserSerializer(serializers.ModelSerializer):
    """
  Serializer of Django's default user
  """
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'username', 'id')


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer of category in post
    """

    class Meta:
        model = Category
        fields = ('title', 'slug')


class TagSerializerField(serializers.ListField):
    """
  Serializer of tag in post
  Get from http://www.django-rest-framework.org/api-guide/fields/#listfield
  """
    child = serializers.CharField()

    def to_representation(self, data):
        tags = data.values('id', 'name', 'slug')
        return tags


class TagSerializer(serializers.ModelSerializer):
    """
  Serializer of tag in list
  """

    # tags = TagSerializerField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        instance = super(TagSerializer, self).create(validated_data)
        instance.tags.set(*tags)
        return instance


class PostListSerializer(serializers.ModelSerializer):
    """
  Serializer of Post in post list
  """
    tags = TagSerializerField()
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'slug', 'author', 'publish_at', 'tags', 'category', 'cover_image')

    def to_representation(self, data):
        representation = super(PostListSerializer, self).to_representation(data)
        representation['content'] = data.get_summary()
        return representation


class PostSerializer(serializers.ModelSerializer):
    """
  Serializer of Post in post detail
  """
    tags = TagSerializerField()
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'slug', 'author', 'publish_at',
                  'tags', 'category', 'cover_image')

    # def to_representation(self, data):
    #     representation = super(PostSerializer, self).to_representation(data)
    #     # representation['content'] = data.get_content_as_markdown()
    #     representation['category'] = data.category.title
    #     return representation


class ActionSummarySerializer(serializers.ModelSerializer):
    """
    Serializer of ActionSummary
    """
    likes = serializers.SerializerMethodField('get_like_count')
    comments = serializers.SerializerMethodField('get_comment_count')

    class Meta:
        model = ActionSummary
        fields = ('likes', 'comments')

    def get_like_count(self, data):
        return data.like_count

    def get_comment_count(self, data):
        return data.comment_count


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer of Like
    """
    # post = PostSerializer()
    author = UserSerializer()

    class Meta:
        model = Like
        fields = ('author', 'create_at', 'canceled')


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer of Comment
    """
    author = UserSerializer()
    create_at = DateTimeTzAwareField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'create_at', 'approved')

