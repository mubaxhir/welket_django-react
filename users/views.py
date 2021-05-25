# Imports from built-in Django stuff
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
  # import flash messages
# import stops user from accessing routes if their not logged in
from django.contrib.auth.decorators import login_required
from . import views
from trading.models import Friend_List
# Imports from apps you've made
# the form you created in forms.py that inherits from Django's UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import *
from trading.models import *
from trading.forms import PostForm
from itertools import chain
import json
import math, random
import base64
from django.contrib import auth
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime,timedelta
from django.forms import model_to_dict
# Create your views here.

# genearting otp for forgot password
def generateOTP() : 
  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = "" 
  
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP

# User Registration form using Djangos built-in User Form
# Register new User
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save users data to database create and save new user from form data
            username = form.cleaned_data.get('username')  # get the username
            password = form.cleaned_data.get('password1')  # get the username
            user = auth.authenticate(username=username, password=password)
            # return HttpResponseRedirect("home_page")

            # show a flash message
            # messages.success(request, f'Account created successfully! Now you can login.')
            # return render(request, 'login')
            if user is not None:
            # correct username and password login the user
                auth.login(request, user)
                return redirect('home_page')
            else:
                print('''
                -----------------------------
                -----------------------------
                -----------------------------''')
        else:
            messages.warning(request, 'Check email. Password should be 8 or more mixed characters.')
            return render(request, 'trading/landing-page.html')

    if request.method == 'GET':
        form = UserRegisterForm()    
        # messages.warning(request, 'Form Validation Failed. Try Again.')
        return render(request, 'trading/landing-page.html')

    return render(request, 'trading/landing-page.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home_page')

        else:
            messages.warning(request, 'Error: Wrong username or password')

    return render(request, 'trading/landing-page.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "Logged Out Successfully!")
    return render(request,'trading/landing-page.html')


# a built-in decorator that requires the user to be logged in to access this view
@login_required
def user_profile(request):
    ######################################
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]
    ######################################
    form = PostForm()
    
    if request.method == 'POST' \
        and request.POST.get("form_name", None) == "post_form":
        
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            form.save()
            new.save()
            return redirect('landing_page')

    ######################################
    if request.is_ajax():
        try:
            # print(request.POST['name'])
            image = request.POST['image']
            if request.POST['name']:
                image_data = image.replace("data:image/png;base64,", "")
                imgdata = base64.b64decode(image_data)
                filename = 'some_image_' + generateOTP() + '.png'
                full_path = f'{settings.BASE_DIR}/media/{filename}'# I assume you have a way of picking unique filenames
                with open(full_path, 'wb') as f:
                    f.write(imgdata)
                profile = Profile.objects.filter(user=request.user).update(image=filename)
                return redirect('user_profile')
        except:
            return redirect('user_profile')
        
    elif request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        user = User.objects.filter(id=request.user.id).first() 
        # User.objects.filter(id=request.user.id).update(first_name=first_name,last_name=last_name,email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile = Profile.objects.filter(user=request.user.id).first()
        profile.description = description
        user.save()
        profile.save()
        # .update(description=description)
        messages.success(request, f'Your account has been updated!')
        # return redirect('user_profile')
        # return {"messege":"success", "code":200}
        return HttpResponse('success 200 ok')
    
    try:
        friend = Friend_List.objects.get(user=request.user).friend_name.all()
    except:
        friend=None

    user_follow = UserFollowing.objects.filter(following_user_id=request.user)
    user_follow_post = UserFollowing.objects.filter(user_id=request.user).values_list('following_user_id',flat=True)
    new_posts = Post.objects.filter(Q(author__in=user_follow_post)|Q(author=request.user)|Q(sharedpost__user__in=user_follow_post)|Q(sharedpost__user=request.user)).order_by('-date_posted','-sharedpost__create_dated')
    posts = sorted(list(set(new_posts)),key= lambda instance:instance.shared_post_time if instance.shared_post_time   else instance.date_posted)[::-1]
    if user_follow is None:
        user_follow = None

    # print(user_follow)
    # for i in current_user:
    #     current.append(i)
    # posts = []
    # user_profile = Profile.objects.get(user=request.user)
    # try:
    #     friends = user_profile.friends.friend_name.all() 
    #     for i in friends:
    #         posts.append(Post.objects.filter(author=i).order_by('-date_posted'))
    #     posts_sorted=[]
    #     for i in posts:
    #         for j in i:    
    #             posts_sorted.append(j) 
    # except:
    #     posts=[]
    #     posts_sorted=[]
 

    # for i in current_user:
    #     posts_sorted.append(i)

    # posts = sorted(list(chain(posts_sorted)),key= lambda instance:instance.date_posted)[::-1]
    # all_ads = advert.objects.all()
    # alist = {}

    # count = 0

    # for i in posts:
    #     if count == 8:
    #         try:
    #             alist['a'+str(len(alist))] = all_ads[random.randint(0,len(all_ads)-1)]
    #         except:
    #             alist['p'+str(len(alist))] = i
    #         count = 0
    #     else:
    #         alist['p'+str(len(alist))] = i
    #         count = count + 1
    
    # blist = []
    # clist = []
    # for i,j in alist.items():
    #     clist.append(j)
    #     if i[0] == 'a':
    #         blist.append(True)
    #     else:
    #         blist.append(False)
    # empty = -1
    # if not blist and not clist:
    #     empty = 1 



    objs = advert.objects.filter(author=request.user)
    context = {
        'ads':objs,
        'user_follow':user_follow,
        'user_follow_post':user_follow_post,
        'friend_List':friend,
        'userzero':userzero,
        'posts': posts,
    }
    # render html from templates folder and pass in data using context
    return render(request, 'users/user_profile.html', context)




def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        user = User.objects.get(email=email)
        otp = generateOTP()
        current_time = timezone.now() + timedelta(minutes=5)
        to_email = user.email
        mail_subject = 'Reset your account password.'   
        context =  {    
                'user': user,
                'otp': otp,   
        }
        message = render_to_string('reset-password-email.html', context ) 
        send_mail(mail_subject,message, 'Info@amzwriters.com', [to_email])
        messages.success(request,'code sent to registered email address')




def profile(request,user):
     ######################################
    user_list = []
    friends_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]


    ######################################
    user_profile = Profile.objects.get(user=user)
    follwers = UserFollowing.objects.filter(user_id=request.user,following_user_id=user).first()
    # print(follwers)
    user_follower = UserFollowing.objects.filter(following_user_id=user)
    request_user_follower = UserFollowing.objects.filter(following_user_id=request.user).values_list('user_id',flat=True)
    requested_user = FriendRequest.objects.filter(sending_user=request.user).values_list('pending_user',flat=True)
    if user_follower is None:
        user_follower = None
    try:
        friends = Friend_List.objects.filter(user=user).values('friend_name')
        for i in friends:
            user = User.objects.get(id=i['friend_name'])
            friends_list.append(user)
        posts =  Post.objects.filter(author=user_profile.user).order_by('-date_posted')
    except:
        friend=None
    # print(friends_list)
    context = {
        'user_profle': user_profile,
        'user_list_json':user_list_json,
        'user_follower':user_follower,
        'request_user_follower':request_user_follower,
        'userzero':userzero,
        'friends':friends_list,
        'requested_user':requested_user,
        'posts':posts,
        'followers':follwers,       
    }
    return render(request, 'users/profile.html', context)

def AddToFollow(request):
    if request.method == 'POST':
        # print(request.POST)
        if request.POST['status'] == 'False':
            follow_user = User.objects.get(id=int(request.POST['id']))
            existed,created = UserFollowing.objects.get_or_create(user_id=request.user,following_user_id=follow_user)
            if created:
                status = True
            elif existed:
                status = True
            context = {
                'status':True
            }
        else:
            follow_user = User.objects.get(id=int(request.POST['id']))
            existed = UserFollowing.objects.filter(user_id=request.user,following_user_id=follow_user).delete()
            context = {
                'status':False
            }      
        
    return JsonResponse(context, safe=False)

def share(request):
    if request.method == 'POST':
        context = None
        post_id = request.POST.get('id')
        user = request.user
        if 'like' in request.POST:
            like = request.POST.get('like')
            post = Post.objects.get(id=post_id)
            existed,created = Share.objects.get_or_create(post=post,user=request.user)
            if created:
                Share.objects.filter(post=post,user=request.user).update(likes=like)
                status = like
                like_count =  Share.objects.filter(post=post,likes=True).count()
            else:
                status = like
                existed.likes = like
                existed.save()
                like_count = Share.objects.filter(post=post,likes=True).count()
            context = {
                'status':status,
                'like_count':like_count
            }
        elif 'comment' in request.POST:
            comment = request.POST.get('comment')
            post = Post.objects.get(id=post_id)
            existed,created = Share.objects.get_or_create(post=post,user=request.user)
            if created:
                status = True
                Share.objects.filter(post=post,user=request.user).update(comments=comment)
                comment_count = Post.objects.filter(id=post_id).values('share__comments').count()
            else:
                status = True
                existed.comments = comment
                existed.save()
                comment_count = Post.objects.filter(id=post_id).values('share__comments').count()
            context = {
                'status':status,
                'comment_count':comment_count
            }
        else:
            post_id = request.POST['id']
            instance = Post.objects.get(id=post_id)
            share_post,created =  SharedPost.objects.get_or_create(post=instance,user=request.user)
            if share_post:
                share_post.create_dated = timezone.now()
                share_post.save()
                Post.objects.filter(id=post_id).update(shared_post_time=timezone.now())
            else:
                created.create_dated = timezone.now()
                created.save()
                Post.objects.filter(id=post_id).update(shared_post_time=timezone.now())
            context = {
                'status':True
            }

        return JsonResponse(context, safe=False)


def show_comments(request):
    if request.method == 'POST':
        post_id = request.POST['id']
        post = Post.objects.get(id=post_id)
        all_comments = Share.objects.filter(post=post)[:30]
        html_rendered = render_to_string('trading/comments.html',{'all_comments': all_comments,'post':post})
        context = {
            'html':html_rendered
        }
    return JsonResponse(context, safe=False)

        
def delete(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        post_to_delete = Post.objects.get(id=post_id)
        if post_to_delete.author == request.user:
            Post.objects.filter(id=post_id).delete()
            status = True
            messages.error(request, f'Post deleted successfully')
        else:
            status = False
            messages.error(request, f'You cannot delete this post')
    return JsonResponse(status, safe=False)

    

#***************** Followers Api *******************
# from django.views import View
# from django.http import HttpResponse
# class Get_followers(View):

#     def get(self, request, *args, **kwargs):
#         print(request.user)
#         users = User.objects.filter(username=request.user)
#         # user_follow_post = UserFollowing.objects.filter(user_id=request.user).values_list('following_user_id',flat=True)
#         context =[]
#         for user in users:
#             user_follow = UserFollowing.objects.filter(following_user_id=user)
#             context.append({
#                 'first_name':user.first_name,
#                 'last_name':user.last_name,
#                 'user_follow':user_follow,
#                 # 'user_follow_post':user_follow_post,
#             })
#         print(context)
#         return HttpResponse(context)
