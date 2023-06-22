import os
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from userQueries.forms import ApplicationForRegistrationForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string




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
            send_mail(subject, email, f'{os.environ.get("EMAIL_HOST_USER")}',
                        [f"{os.environ.get('ADMIN_EMAIL', default='admin@vashemore.ru')}"], fail_silently=False)
         except BadHeaderError:

            return HttpResponse('Invalid header found.')
         form.save()
         return JsonResponse({'success': True, "reload": True, "message": "Заявка успешно отправлена!"})
      else:
         return JsonResponse({"error": True, "message": form.errors})
   return HttpResponseBadRequest()