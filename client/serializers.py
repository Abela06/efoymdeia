from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Video, Channel, Viewer, Section, Page, Category, FacebookPost


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    channelCategory = CategorySerializer()

    class Meta:
        model = Channel
        fields = ('channelTitle', 'channelCategory')


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    channel = ChannelSerializer()
    category = CategorySerializer()

    class Meta:
        model = Video
        fields = ('videoId', 'title', 'channel', 'publishedAt', 'thumbnailsLow', 'thumbnailsHigh', 'thumbnailsMedium',
                  'thumbnailsLocal', 'url', 'description',
                  'ext', 'view_count', 'like_count', 'dislike_count', 'video', 'category')
        depth = 1


class FacebookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refreshToken'] = str(refresh)
        data.pop('refresh', None)  # remove refresh from the payload
        data.pop('access', None)  # remove refresh from the payload
        data['accessToken'] = str(refresh.access_token)
        # Add extra responses here
        data['username'] = self.user.username
        data['email'] = self.user.email
        # data['kind'] = self.user.kind
        # data['date'] = datetime.date.today()
        # data['expires']=timedelta(minutes=5)
        return data
