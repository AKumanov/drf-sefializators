from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    MAX_LENGTH = 100
    id = serializers.IntegerField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']

    def create(self, validated_data):
        """
        Create and return a new 'Snippet', given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing 'Snippet', given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        read_only=True
    )

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']


class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


comment = Comment(email="test@abv.bg", content="foo bar")


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(
        max_length=200,
    )
    created = serializers.DateTimeField()

    def create(self, validated_data):
        # if this is a model, we can save it as well
        # return Comment.objects.create(**validated_data)
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        # instance.save()
        return instance


# overriding save method
class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        # send_email(from=email, message=message)


# Field level validation
class BlogPost:
    def __init__(self, title, content, likes_number):
        self.title = title
        self.content = content
        self.likes_number = likes_number


# Validators
def multiple_of_ten(value, error_msg):
    if not value % 10 == 0:
        raise serializers.ValidationError("Not a multiple of ten!")


class BlogPostSerializer(serializers.Serializer):
    __INVALID_BLOG_POST_TITLE_ERROR_MESSAGE = "Invalid Blog Post Title"
    title = serializers.CharField(
        max_length=100
    )
    content = serializers.CharField()
    likes_number = serializers.IntegerField(
        validators=[multiple_of_ten]
    )

    @classmethod
    def validate_title(cls, value):
        """
        Check that the blog post is about Django.
        :param value: title
        :return: returns the value or exception depending on validation condition
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError(cls.__INVALID_BLOG_POST_TITLE_ERROR_MESSAGE)
        return value

    # Object-level validation
    def validate(self, data):
        """check title"""
        self.validate_title(data['title'])
        """check content"""
        if len(data['content']) < 3:
            raise serializers.ValidationError('Content too short')

        return data
