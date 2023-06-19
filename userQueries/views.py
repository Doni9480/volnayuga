from django.http import JsonResponse, HttpResponseBadRequest
from userQueries.forms import ApplicationForRegistrationForm


def application_for_registration(request):
   if request.method == "POST" and request.is_ajax():
      form = ApplicationForRegistrationForm(request.POST)
      if form.is_valid():
         form.save()
         return JsonResponse({'success': True, "reload": False, "message": "Заявка успешно отправлено!"})
      else:
         return JsonResponse({"error": True, "message": "Данные уже существуют!"})
   return HttpResponseBadRequest()