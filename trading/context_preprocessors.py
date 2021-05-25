from .models import Friend_List,FriendRequest


def friends(request):
    friends = None
    friend_request = None

    if request.user.is_authenticated:
        try:
            friend_request = FriendRequest.objects.filter(status=False,pending_user=request.user)
            friends = Friend_List.objects.get(user=request.user).friend_name.all()
        except Exception as err:
          print(err)

    return {"friends": friends,"friend_request":friend_request}
