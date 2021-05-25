from rest_framework import serializers
from .models import *
from users.models import *
from chat.models import Message
from django.contrib.auth.models import User
from django.conf import settings


# class FriendRelatedField(serializers.RelatedField):
    
#     def display_value(self, instance):
#         return instance

#     def to_representation(self, value):        
#         return str(value)

#     def to_internal_value(self, data):
#         return User.objects.get(username=data)

class FriendOnlySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        text = str(Profile.objects.filter(user=obj).first().description)
        return text

    class Meta:
        model = User
        fields = ['first_name','last_name','username','image',"description"]

    def get_image(self, obj):
        # image = "http://localhost:8000"+str(Profile.objects.filter(user=obj).first().image.url)
        image = settings.ALLOWED_HOSTS[0]+str(Profile.objects.filter(user=obj).first().image.url)
        return image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    def validate_parent(self, value):
        print(self.context['request'].user)
        return value 

    class Meta:
        model = Profile
        fields = ("id",'user','user_name','friends',"image","first_name","last_name",'email',"description","followers","followings")
        # fields = '__all__'

    def get_followers(self, obj): 
        followers =  UserFollowing.objects.filter(following_user_id=obj.user)
        followers_names =[]
        for follower in followers:
            follow_profile = Profile.objects.filter(username=follower.user_id).first()
            user=User.objects.filter(username=follower.user_id).first()
            if (str(follower.user_id) not in followers_names) and (str(follower.user_id) != str(obj.user)) and (follow_profile != None):
                follow_profile = Profile.objects.filter(username=follower.user_id).first()
                user=User.objects.filter(username=follower.user_id).first()
                context = {
                    'username':str(follower.user_id),
                    'first_name':str(user.first_name),
                    'last_name':str(user.last_name),
                    # 'image':"http://localhost:8000/media/"+str(follow_profile.image)
                    'image':settings.ALLOWED_HOSTS[0]+"/media/"+str(follow_profile.image),
                    'description':str(follow_profile.description)
                }
                followers_names.append(context)
        return followers_names

    def get_followings(self, obj):
        followings = UserFollowing.objects.filter(user_id=obj.user)
        follow_names =[]
        for follower in followings:
            follower_profile = Profile.objects.filter(username=follower.following_user_id).first()
            user=User.objects.filter(username=follower.following_user_id).first()
            if (str(follower.following_user_id) not in follow_names)  and (follower_profile != None):
                context = {
                    'username':str(follower.following_user_id),
                    'first_name':str(user.first_name),
                    'last_name':str(user.last_name),
                    # 'image':"http://localhost:8000/media/"+str(follower_profile.image)
                    'image':settings.ALLOWED_HOSTS[0]+"/media/"+str(follower_profile.image),
                    'description':str(follower_profile.description)
                }
                follow_names.append(context)
        return follow_names

    


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_first_name = serializers.ReadOnlyField(source='author.first_name')
    author_last_name = serializers.ReadOnlyField(source='author.last_name')
    class Meta:
        model = Post
        fields = ['id','author','author_username','author_first_name','author_last_name',"author_image",'img','video','content','date_posted']


class FriendSerializer(serializers.ModelSerializer):
    # friend_name = FriendRelatedField(
    #         queryset=User.objects.all(),
    #         many=True
    #     )
    # friend_name = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    user_name = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    image = serializers.SerializerMethodField()
    friend_name = FriendOnlySerializer(many=True, read_only=True)
    description = serializers.SerializerMethodField()


    class Meta:
        model = Friend_List
        fields = ['id','user','user_name','first_name','last_name',"description",'image','friend_name']
        # fields = '__all__'

    def get_image(self, obj):
        # image = "http://localhost:8000"+str(Profile.objects.filter(user=obj.user).first().image.url)
        image = settings.ALLOWED_HOSTS[0]+str(Profile.objects.filter(user=obj.user).first().image.url)
        return image

    def get_description(self, obj):
        text = str(Profile.objects.filter(user__username=obj).first().description)
        return text

class ChatSerializer(serializers.ModelSerializer):
    # author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Message
        fields = ['id','sender','receiver','message','timestamp','is_read']

