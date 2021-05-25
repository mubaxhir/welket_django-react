from django.contrib import admin
from .models import Post , Friend_List , advert,UserFollowing,Share,FriendRequest,SharedPost
# Register your models here.
admin.site.register(Post)
admin.site.register(Friend_List)
admin.site.register(advert)
admin.site.register(UserFollowing)
admin.site.register(Share)
admin.site.register(FriendRequest)
admin.site.register(SharedPost)
