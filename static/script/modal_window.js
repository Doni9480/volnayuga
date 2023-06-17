$('.open-login-modal').click(() => {
   $('#registration-window').removeClass("modal-window__open");
   $('nav').hasClass("nav-responsive") && burgerMenu();
   $('body').css('overflow', 'hidden');
   $('#login-window').addClass("modal-window__open");
});
$('#open-register-modal').click(() => {
   $('#login-window').removeClass("modal-window__open");
   $('body').css('overflow', 'hidden');
   $('#registration-window').addClass("modal-window__open");
});

$('.modal-window__close').click(() => {
   $('body').css('overflow', 'auto');
   $('#login-window').removeClass("modal-window__open");
});
$('.modal-window__close').click(() => {
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
   $('#login-window form').submit((event) => {
      event.preventDefault();
      var formData = {
         username: $('#id_username').val(),
         password: $('#id_password').val(),
         // csrftoken: getCookie('csrftoken')
      }
      console.log(formData);
      $.ajax({
         type: "POST",
         url: `/accounts/login/`,
         data: formData,
         dataType: "json",
         encode: true,
         headers: {'X-CSRFToken': getCookie('csrftoken')}
      }).done(function (data) {
         if (data?.error === true){
            $("#msg").css({'display': 'block', 'color': 'red'});
            $("#msg").empty();
            $("#msg").append(data.message);
         } else if (data?.success === true){
            $("#msg").css({'display': 'block', 'color': 'green'});
            $("#msg").empty();
            $("#msg").append(data.message);
            if(data.reload === true){
               location.reload();
            }
         }
      });
   })


   $('#registration-window form').submit((event) => {
      event.preventDefault();
      var formData = {
         email: $('#id_email').val(),
         phone: $('#id_phone').val(),
      }
      console.log(formData);
      $.ajax({
         type: "POST",
         url: `/user_queries/application_registration/`,
         data: formData,
         dataType: "json",
         encode: true,
         headers: {'X-CSRFToken': getCookie('csrftoken')}
      }).done(function (data) {
         console.log(data);
         if (data?.error === true){
            $("#registration-window #msg").css({'display': 'block', 'color': 'red'});
            $("#registration-window #msg").empty();
            $("#registration-window #msg").append(data.message);
         } else if (data?.success === true){
            $("#registration-window #msg").css({'display': 'block', 'color': 'green'});
            $("#registration-window #msg").empty();
            $("#registration-window #msg").append(data.message);
            if(data.reload === true){
               location.reload();
            }
         }
      });
   })
})