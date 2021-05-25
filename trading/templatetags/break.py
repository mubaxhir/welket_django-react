from django import template
from trading.models import Friend_List,Share,Post,SharedPost
from django.contrib.auth.models import User

register = template.Library()

@register.filter('break')
def break_(value,id):
    
    instance  =  Friend_List.objects.get(user=id)
    try:
        instance.friend_name.get(username=(value))
        return True
    except:
        return False


@register.filter('custom_filter')
def custom_filter_(self,user):
    post = Post.objects.get(id=user)
    user = User.objects.get(id=self.id)
    instance  =  Share.objects.filter(post=post,user=user,likes=True).first()
    if instance:
        return True
    else:
        return False


@register.filter('shared_post')
def shared_post_(self,user):
    # print(user)
    post = Post.objects.get(id=user)
    user = User.objects.get(id=self.id)
    instance  =  SharedPost.objects.filter(post=post,user=user).order_by('create_dated')
    # print(instance)
    if instance:
        return instance
    else:
        return False