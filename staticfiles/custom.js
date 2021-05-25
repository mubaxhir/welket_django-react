$(document).ready(function() {
    // $('.form-sing').on('show.bs.tab', function (e) {    	
    //     if (e.relatedTarget === undefined) {    
    //       $($(e.target).attr('href')).slideDown('fast');
    //     }
    //     else {
    //       $($(e.relatedTarget).attr('href')).slideUp({ duration: 'fast', queue: true,
    //         done: function() {
    //           $($(e.target).attr('href')).slideDown('fast');
    //         }
    //       });
    //     }	
    // });

    // $('.form-sing a[data-toggle="tab"]').on('show.bs.tab', function (e) {
    //     $($(e.target).attr('href')).hide();
    //   })
    //   $('.form-sing a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    //     $($(e.target).attr('href')).slideDown(1000);
    //   })

      window.onscroll = function() {myFunction()};

    var header = document.getElementById("myHeader");
    var sticky = header.offsetTop;

    function myFunction() {
      if (window.pageYOffset > sticky) {
        header.classList.add("sticky");
      } else {
        header.classList.remove("sticky");
      }
    }
});