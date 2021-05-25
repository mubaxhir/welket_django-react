from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib.auth.models import User
import math
import ckeditor
# import User model that already comes with Django

class advert(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500,blank=True)
    linked = models.URLField(blank=True)
    img = models.ImageField(blank=True,upload_to='ad_images')
    video = models.FileField(blank=True,upload_to='ad_videos')
    active = models.BooleanField(default=False)
    start = models.BigIntegerField(default=0)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Friend_List(models.Model):
    user = models.ForeignKey(User , on_delete= models.CASCADE)
    friend_name = models.ManyToManyField(User,related_name='list')
    username = models.CharField(max_length=500,blank=True)

    def save(self, *args, **kwargs):
        self.username = self.user.username
        super(Friend_List, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username

from users.models import Profile

# Create your models here.
class Post(models.Model):
    # title = models.CharField(max_length=254)
    
    img = models.ImageField(blank=True,upload_to='post_images')
    author_image = models.ImageField(blank=True,upload_to='post_images')
    video = models.FileField(blank=True,upload_to='post_videos')
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_post_time = models.DateTimeField(auto_now_add=True,null=True)

    def save(self, *args, **kwargs):
        user = Profile.objects.get(user=self.author)
        self.author_image = user.image
        self.shared_post_time = self.date_posted
        super(Post, self).save(*args, **kwargs)




    def __str__(self):
        return self.author.username

    def time_since_posted(self):
        now = timezone.now()

        diff = now - self.date_posted

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return self.date_posted.strftime("%b %d, %Y")

            else:
                return self.date_posted.strftime("%b %d, %Y")

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return self.date_posted.strftime("%b %d, %Y")

            else:
                return self.date_posted.strftime("%b %d, %Y")

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return self.date_posted.strftime("%b %d, %Y")

            else:
                return self.date_posted.strftime("%b %d, %Y")

    def comments_count(self):
        coment_count = 0
        commentss = self.share_set.filter(post_id=self.id).values_list('comments',flat=True)
        res = [] 
        for val in commentss: 
            if val != None : 
                res.append(val)
        if len(res) > 0:
            return len(res)
        else:
            return coment_count

    def likes_count(self):
        #Your filter criteria can go here.
        likes = self.share_set.filter(post_id=self.id,likes=True)
        return likes.count()

class VerifyOtp(models.Model):
    otp = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expire_time = models.TimeField()

    def __str__(self):
        return self.user.username

    def clean():
        VerifyOtp.objects.all().delete()


class UserFollowing(models.Model):
    #user follow table
    user_id = models.ForeignKey(User, related_name="following",on_delete= models.CASCADE)

    following_user_id = models.ForeignKey(User, related_name="followers",on_delete= models.CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"

class Share(models.Model):
    post = models.ForeignKey(Post, verbose_name=("Post"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("User"), on_delete=models.CASCADE)
    likes = models.BooleanField(("Likes"),default=False,null=True)
    comments = models.CharField(("Comments"), max_length=1000,null=True)
    share_url = models.URLField(("Share"), max_length=200,null=True)
    create_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    pending_user = models.ForeignKey(User, verbose_name=("Request Sent to User"), on_delete=models.CASCADE)
    sending_user = models.ForeignKey(User, verbose_name=("Sending  user"),related_name="sending_user", on_delete=models.CASCADE,null=True)
    status = models.BooleanField(("Status"),default=False)
    sent_time = models.DateTimeField(("Sent Time"),auto_now_add=True)

    def __str__(self):
        return self.pending_user.username


class SharedPost(models.Model):
    post = models.ForeignKey(Post, verbose_name=("Shared Post"), on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("Shared by"), on_delete=models.CASCADE)
    create_dated = models.DateTimeField(("Shared time"),null=True)


    def __str__(self):
        return self.user.first_name +' shared the post '+self.post.content

    
    def time_since_posted(self):
        now = timezone.now()

        diff = now - self.create_dated

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return self.create_dated.strftime("%b %d, %Y")

            else:
                return self.create_dated.strftime("%b %d, %Y")

        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return self.create_dated.strftime("%b %d, %Y")

            else:
                return self.create_dated.strftime("%b %d, %Y")

        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return self.create_dated.strftime("%b %d, %Y")

            else:
                return self.create_dated.strftime("%b %d, %Y")