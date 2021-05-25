function AddToFollow(url,id) { 
  console.log(id);
  var status = document.getElementById('status'+id).value;
  console.log(status);
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,'status':status },
    success: function(status) {
      console.log(status.status);
      if(status.status == true){
        document.getElementById('status'+id).value = 'True';
        document.getElementById('status'+id).innerHTML = 'Following';
      }
      else {
        document.getElementById('status'+id).value = 'False';
        document.getElementById('status'+id).innerHTML = 'Follow';
      }
    }
  });
}

function approve(url,id) { 
  var status = document.getElementById('status'+id).value;
  console.log(status);
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,'status':status },
    success: function(status) {
      location.reload(true);
    }
  });
}

function reject(url,id) { 
  var status = document.getElementById('status'+id).value;
  console.log(status);
  $.ajax({
    type: 'POST',
    url: url,
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data: {'id':id,'status':status },
    success: function(status) {
      location.reload(true);
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
      console.log(status)
      if(status.status == "True"){
        icon.classList.remove("fa-thumbs-o-up");
        icon.classList.add("fa-thumbs-up");
        document.getElementById('like'+id).value = "False";
        follow_count.innerHTML = status.like_count ;
      }
      else{
        icon.classList.remove("fa-thumbs-up");
        icon.classList.add("fa-thumbs-o-up");
        console.log(icon);
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
        window.reload();
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