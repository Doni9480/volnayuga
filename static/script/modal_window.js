let redirect = false;

let openWLogin = () => {
   $(".msg").empty();
   $('#registration-window').removeClass("modal-window__open");
   $('nav').hasClass("nav-responsive") && burgerMenu();
   $('body').css('overflow', 'hidden');
   $('#login-window').addClass("modal-window__open");
}

$('.open-login-modal').on('click', () => {
   openWLogin();
});
$('#rent-buttnon-id').on('click', () => {
   redirect =true;
   openWLogin();
});
$('#open-register-modal').on('click', () => {
   $(".msg").empty();
   $('#login-window').removeClass("modal-window__open");
   $('body').css('overflow', 'hidden');
   $('#registration-window').addClass("modal-window__open");
});

$('.modal-window__close').on('click', () => {
   $('body').css('overflow', 'auto');
   $('#login-window').removeClass("modal-window__open");
});
$('.modal-window__close').on('click', () => {
   $('body').css('overflow', 'auto');
   $('#registration-window').removeClass("modal-window__open");
});

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

$(document).ready(() => {
   $(".phone-maske").inputmask({"mask": "+7 (999) 999-99-99"});

   $('#login-window form').submit((event) => {
      event.preventDefault();
      var formData = {
         username: $('#id_username').val(),
         password: $('#id_password').val(),
      }
      $.ajax({
         type: "POST",
         url: `/accounts/login/`,
         data: formData,
         dataType: "json",
         encode: true,
         headers: {'X-CSRFToken': getCookie('csrftoken')}
      }).done(function (data) {
         if (data?.error === true){
            $("#login-window #msgl_username").css({'display': 'block', 'color': 'red'});
            $("#login-window #msgl_username").empty();
            if (data.message?.__all__){
               $(".msg").append(data.message.__all__);
            }
         } else if (data?.success === true){
            $("#login-window #msgl_username").css({'display': 'block', 'color': 'green', 'margin-top': '15px'});
            $("#login-window #msgl_username").empty();
            if (data.message){
               $("#login-window #msgl_username").append(data.message);
            }
            if(data.reload === true){
               if(redirect){
                  var link = $("#rent-buttnon-id").data('link');
                  $(location).attr('href',link);
               }else{
                  location.reload();
               }
            }
         }
      });
   })


   $('#registration-window form').submit((event) => {
      event.preventDefault();
      var formData = {
         email: $('#registration-window #id_email').val(),
         phone: $('#registration-window #id_phone').val(),
         name: $('#registration-window #id_username_reg').val(),
      }
      $.ajax({
         type: "POST",
         url: `/user_queries/application_registration/`,
         data: formData,
         dataType: "json",
         encode: true,
         headers: {'X-CSRFToken': getCookie('csrftoken')}
      }).done(function (data) {
         if (data?.error === true){
            $("#registration-window .msg").css({'display': 'block', 'color': 'red'});
            $("#registration-window .msg").empty();
            if (data.message?.name?.length){
               $("#msgr_username").append(data.message.name[0]);
            }
            if (data.message?.email?.length){
               $("#msgr_email").append(data.message.email[0]);
            }
            if (data.message?.phone?.length){
               $("#msgr_phone").append(data.message.phone[0]);
            }
         } else if (data?.success === true){
            $("#registration-window .msg").css({'display': 'block', 'color': 'green', 'margin-top': '15px'});
            $("#registration-window .msg").empty();
            if (data.message){
               $("#registration-window #msgr_phone").append(data.message);
            }
            if(data.reload === true){
               location.reload();
            }
         }
      });
   })
})