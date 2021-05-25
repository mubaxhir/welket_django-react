from django.shortcuts import render, redirect
from datetime import datetime,timedelta,timezone
from .models import *  # import model so you can display the data in a view
from users.models import *
from django.contrib import messages
from chat.models import Message
# import stops user from accessing routes if their not logged in
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from .models import Post , advert
from django.contrib.auth.models import User
from .forms import PostForm , advertform
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import json
import time
import random
import math
#payment gateway
from bfinder import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
#reference Finder
import requests 
from django.http import JsonResponse
from bs4 import BeautifulSoup
import re

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

# Landing Page
def landing_page(request):
    # if the user is logged in and tries to access '' route (landing_page), redirect to users home content page
    if request.user.is_authenticated:
        return redirect('home_page')
    # render html from templates folder
    return render(request, 'trading/landing-page.html')

from itertools import chain
# Home Page (Newsfeed, whatever, main content NOT THE USER PROFILE)
# a built-in decorator that requires the user to be logged in to access this view
@login_required
def home_page(request):
    #######################################
    test_ads()
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]

    ########### Post Form #################
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(request.FILES)
        if not request.POST.get('content') and not request.FILES.get('img') and not request.FILES.get('video'):
            messages.warning(request, "Information: Empty posts are not allowed.")
            return redirect('home_page')

        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            form.save()
            new.save()
            return redirect('landing_page')

    #######################################
    current = []
    current_user = Post.objects.filter(author=request.user)
    for i in current_user:
        current.append(i)
    posts = []
    user_profile = Profile.objects.get(user=request.user)
    user_follow_post = UserFollowing.objects.filter(user_id=request.user).values_list('following_user_id',flat=True)
    shared_post = SharedPost.objects.filter(user=request.user).values_list('post_id',flat=True)
    share_posts = SharedPost.objects.filter(user=request.user)
    try:
        posts.append(Post.objects.filter(Q(author__in=user_follow_post)|Q(author=request.user)).order_by('-date_posted'))
        posts.append(Post.objects.filter(Q(sharedpost__user__in=user_follow_post)|Q(sharedpost__user=request.user)).order_by('-sharedpost__create_dated'))
        posts_sorted=[]
        for i in posts:
            for j in i:
                posts_sorted.append(j) 

        new_post_sorted = list(set(posts_sorted))

        
    except :
           posts=[]
           posts_sorted=[]


    # import pdb;pdb.set_trace();
    posts = sorted(list(chain(new_post_sorted)),key= lambda instance:instance.shared_post_time)[::-1]
   
    ############################################

    all_ads = advert.objects.all()
    alist = {}

    count = 0

    for i in posts:
        if count == 8:
            try:
                alist['a'+str(len(alist))] = all_ads[random.randint(0,len(all_ads)-1)]
            except:
                alist['p'+str(len(alist))] = i
            count = 0
        else:
            alist['p'+str(len(alist))] = i
            count = count + 1
    
    blist = []
    clist = []
    for i,j in alist.items():
        clist.append(j)
        if i[0] == 'a':
            blist.append(True)
        else:
            blist.append(False)
    empty = -1
    if not blist and not clist:
        empty = 1 

    context = {
        'posts': zip(blist,clist),
        'users': User.objects.all() ,
        'user_list_json': user_list_json,
        'user_profile':user_profile,
        'userzero':userzero,
        'shared_posted':shared_post,
        'shareds':share_posts,
        'form':form,
        'empty': empty,
    }

    return render(request, 'trading/home.html', context)



@login_required
def PostView(request):
      ######################################
    test_ads()
    ######################################
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            form.save()
            new.save()
            return redirect('landing_page')
    try:
        ad = advert.objects.all()[random.randint(0,len(advert.objects.all())-1)]
    except:
        ad = advert.objects.all()

    context = {
        'form':form,
        'user_list_json':user_list_json,
        'userzero':userzero,
        'ad':ad
    }
     
    return render(request,'trading/post.html',context)

@csrf_exempt
@login_required
def search(request):
    ######################################
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]
    

    ######################################
    query=request.POST.get('query',None)
    user=User.objects.all()
    if query is not None:
        user=user.filter(
        Q(username__icontains=query)
        ).exclude(Q(username__icontains=request.user.username))
    try:
        user_follow = UserFollowing.objects.filter(user_id=request.user,following_user_id__in=user).values_list('following_user_id',flat=True)
        print(user_follow)
    except:
        user_follow = None

    try:
        friend_list = Friend_List.objects.get(user=request.user).friend_name.all(),
    except ObjectDoesNotExist:
        friend_list = None
    ############################################
    action = request.POST.get('action')
    

    if action:
        ids= request.POST.get('id')
        print(ids)
        name = User.objects.get(id=ids)
        try:
            instance=FriendRequest.objects.get(pending_user=name,sending_user=request.user)
            instance.sent_time = timezone.now()
            instance.save()
        except ObjectDoesNotExist:
            FriendRequest.objects.create(pending_user=name,sending_user=request.user,sent_time=timezone.now())
   
    ################################################
    context={
        'friend_list':friend_list,
        'users':user,
        'query':query,
        'user_follow':user_follow,
        'user_list_json':user_list_json,
        'userzero':userzero
    }

    return render(request,'trading/search.html',context)


def friendrequest(request):
    if request.method == "POST":
        if request.POST['status'] == 'True':
            user_id = request.POST['id']
            accepted_user = FriendRequest.objects.filter(pending_user=request.user,sending_user=user_id).first()
            request_accepted_user = User.objects.get(id=user_id)
            try:
                instance=Friend_List.objects.get(user=request.user)
                instance.friend_name.add(request_accepted_user)
                instances=Friend_List.objects.filter(user=request_accepted_user).first()
                if instances is not None:
                    instances.friend_name.add(request.user)
            except ObjectDoesNotExist:
                instance=Friend_List.objects.create(user=request.user)
                pro=Profile.objects.get(user=request.user)
                pro.friends=instance
                pro.save()
            
                print('success')
                instance.friend_name.add(request_accepted_user)
                instances=Friend_List.objects.create(user=request_accepted_user)
                pros=Profile.objects.get(user=user_id)
                pros.friends=instances
                pros.save()
            
                print('success')
                instance.friend_name.add(request.user)

            accepted_user.delete()
            context = {
                'status':True
            }
        else:
            user_id = request.POST['id']
            accepted_user = FriendRequest.objects.filter(pending_user=request.user,sending_user=user_id).update(status=True)
            context = {
                'status': True
            }
        return JsonResponse(context, safe=False)

def forgot_password(request):
    if request.method == "POST":
        VerifyOtp.clean()
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        otp = generateOTP()
        current_time = timezone.now() + timedelta(minutes=5)
        VerifyOtp.objects.get_or_create(otp=otp,user=user,expire_time=current_time)
        to_email = user.email
        mail_subject = 'Reset your account password.'   
        context =  {    
                'user': user,
                'otp': otp,   
        }
        message = render_to_string('trading/reset-password-email.html', context ) 
        send_mail(mail_subject,message,'testuser@conxr.com', [to_email])
        context = {
            'user':user
        }
        return render(request,'trading/verifyotp.html',context)

def verifyotp(request):
    if request.method == "POST":
        print(request.POST)
        digit1 = request.POST.get('digit1')
        digit2 = request.POST.get('digit2')
        digit3 = request.POST.get('digit3')
        digit4 = request.POST.get('digit4')
        otp = digit1+digit2+digit3+digit4
        try:
            verify = VerifyOtp.objects.get(otp=otp)
            context = {
                'user':verify.user
            }
            return render(request,'trading/forgetps.html',context)
        except:
            messages.error(request, "Otp is invalid please try again")
            return render(request,'trading/verifyotp.html')


def ResetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['verfiypassword']
        if password == confirm_password :
            user = User.objects.get(id=request.POST['user'])
            user.set_password(password)
            user.save()
            return redirect('/')
        else:
            messages.error(request, "Password did not match ")
        


@login_required
def Friendlist(request):
     ######################################
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]


    ######################################
    ids= request.POST.get('id')
    # print(ids)
    name = User.objects.get(id=ids)
    try:
        instance=Friend_List.objects.get(user=request.user)
        instance.friend_name.add(name)
    except ObjectDoesNotExist:
        instance=Friend_List.objects.create(user=request.user)
        pro=Profile.objects.get(user=request.user)
        pro.friends=instance
        pro.save()
        instance.friend_name.add(name)

    context = {
      'name':name,
      'user_list_json':user_list_json,
      'userzero':userzero
    }
     
    return render(request,'trading/Added.html',context)


@login_required
def adView(request):
      ######################################
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]

    ######################################
    form = advertform()
    if request.method == 'POST':
        form = advertform(request.POST,request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.start = time.time()
            form.save()
            new.save()
            try:
                charge = stripe.Charge.create(
                    amount='1500',
                    currency='usd',
                    description='Payment For Add',
                    source=request.POST['stripeToken']
                )
            except:
                objs = advert.objects.last()
                objs.delete()
            return redirect('/')

    context = {
        'form':form,
        'user_list_json':user_list_json,
        'userzero':userzero

    }
     
    return render(request,'trading/advert.html',context)


def test_ads():
    adslist = advert.objects.all()
    a = (60 * 60) * 24
    for i in adslist:
        if (time.time()-i.start) >= a:
            i.delete()
    return

@login_required
def addash(request):
    user_list = []
    for i in User.objects.all():
        user_list.append(i.username)
    user_list_json=json.dumps(user_list)
    userzero = User.objects.all()[0]

    ######################################

    objs = advert.objects.filter(author=request.user)


    context = {
        'ads':objs,
        'user_list_json':user_list_json,
        'userzero':userzero

    }
     
    return render(request,'trading/dash.html',context)

@login_required
def countclick(request,id):
    obj = advert.objects.get(pk=id)
    obj.clicks = obj.clicks + 1
    obj.save()
    return redirect(obj.linked)

####################### Reference Finder View ###################
#********* Parent Function**********#
def reference_finder(value):
  
    print(value)
    
    headers_Get = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    q=value

    request = requests.Session()
    q_search = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q_search + '&ie=utf-8&oe=utf-8'
    page = request.get(url, headers=headers_Get)

    soup = BeautifulSoup(page.text, "html.parser")
    response = soup.find_all('div',class_='rc')
    first_three = []
    matching = []
    for i in response:
        first_three.append(i.find('a').attrs['href'])
    return first_three
#***********************************#
import json
from django.forms.models import model_to_dict

def reference(request,id):
    post_data = Post.objects.get(id=id)
    result = reference_finder(post_data.content)
    for i in range(0,len(result)):
        result[i]="<a target='_blank' href= {}><p>{}</p></a>".format(result[i],result[i])
    print(result)
    return JsonResponse(result, safe=False)

########################## REST API VIEWS ##############################
from .serializers import *
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# *********** Profile Detail *********
class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__username','user',)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    lookup_url_kwarg = 'user'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# ********* Post Api *****************
class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('author__username',)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@csrf_exempt
def posts_list(request):
      
        print(request.method)
        current = []
        current_user = Post.objects.filter(author=request.user)
     

        for i in current_user:
            current.append(i)
        posts = []
        user_profile = Profile.objects.get(user=request.user)
        print('###### USER PROFILE #########')
        print(user_profile)

        try:
            friends = Friend_List.objects.get(user=request.user).friend_name.all() 
            print('#############')
            print(friends)
            print('TRY BLOCK')
            for i in friends:
                posts.append(Post.objects.filter(author=i).order_by('-date_posted'))
                print('#############')
                print(i)
                print('#############')
            posts_sorted=[]
            for i in posts:
                for j in i:
                    posts_sorted.append(j) 
        except Exception as e:
            print(e)
            posts=[]
            posts_sorted=[]
        for i in current_user:
            posts_sorted.append(i)
        posts = sorted(list(chain(posts_sorted)),key= lambda instance:instance.date_posted)[::-1]

        print(posts)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return JsonResponse(data = {"Posts": serializer.data}, status = 200)

# *********** Friends Api **************
class FriendViewset(viewsets.ModelViewSet):
    queryset = Friend_List.objects.all()
    serializer_class = FriendSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user__username','profile__username')

class FriendListDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'username'
    lookup_url_kwarg = 'user_name'
    serializer_class = FriendSerializer
    queryset = Friend_List.objects.all()

# ************** Search Api ***************

class SearchAPIView(generics.ListCreateAPIView):
    search_fields = ['user__username',]
    filter_backends = (filters.SearchFilter,)
    queryset = Friend_List.objects.all()
    serializer_class = FriendSerializer


#**************** Message Api ***************

class ChatAPIView(generics.ListCreateAPIView):

    queryset = Message.objects.all()
    serializer_class = ChatSerializer

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Message.objects.all()




    
  