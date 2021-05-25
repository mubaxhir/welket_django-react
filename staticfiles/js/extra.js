function AddToFollow(url,id) { 
  var status = document.getElementById('status').value;
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,'status':status },
    success: function(status) {
      if(status == true){
        document.getElementById('status').innerHTML = 'Following';
      }
      else {
        document.getElementById('status').innerHTML = 'Follow';
      }
    }
  });
}

function like(url,id) { 
  var like = document.getElementById('like'+id).value;
  console.log(like);
  var icon = document.getElementById('icon-like-'+id);
  console.log(icon);
  var follow_count = document.getElementById('count-likes-'+id);
  console.log(follow_count);
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,'like':like },
    success: function(status) {
      if(status.status == "True"){
        icon.classList.toggle("fa-thumbs-up");
        document.getElementById('like'+id).value = "False";
        follow_count.innerHTML = status.like_count ;
      }
      else{
        icon.classList.toggle("fa-thumbs-o-up");
        document.getElementById('like'+id).value = "True";
        follow_count.innerHTML = status.like_count ;
      }
    }
  });
}


function all_comments(url,id) { 
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id},
    success: function(context) {
      $('#comment-body').html(context.html);
      $("#CommentModalCenter").modal();

    }
  });
}


function comment(url,id) { 
  var comment = document.getElementById('add_comment').value;
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,
          'comment':comment },
    success: function(status) {
      if(status == true){
        document.getElementById('status').innerHTML = 'Following';
      }
    }
  });
}

function del(url) { 
  var id = document.getElementById('post').value;
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id },
    success: function(status) {
      if(status == true){
        location.reload(true);
      }
    }
  });
}


function share(url,id) { 
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id },
    success: function(status) {
      location.reload(true);
    }
  });

}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}