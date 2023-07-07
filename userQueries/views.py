import os
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from userQueries.forms import ApplicationForRegistrationForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from VolnaYuga.settings import ADMINS




def application_for_registration(request):
   if request.method == "POST" and request.is_ajax():
      form = ApplicationForRegistrationForm(request.POST)
      if form.is_valid():
         subject = f"Заявка на регистрацию - {form.cleaned_data['name']}"
         email_template_name = "userQueries/registration_request.txt"
         c = {
            "email": form.cleaned_data['email'],
            'name': form.cleaned_data['name'],
            'phone': form.cleaned_data['phone'],
         }
         email = render_to_string(email_template_name, c)
         try:
            send_mail(
               subject=subject, 
               message=email, 
               from_email=f'{os.environ.get("EMAIL_HOST_USER")}',
               recipient_list=[ADMINS[0][1]], fail_silently=False)
         except BadHeaderError:

            return HttpResponse('Invalid header found.')
         form.save()
         return JsonResponse({'success': True, "reload": True, "message": "Ваша заявка принята! Мы свяжемся с Вами в течении 24 часов."})
      else:
         return JsonResponse({"error": True, "message": form.errors})
   return HttpResponseBadRequest()