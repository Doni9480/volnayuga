from django.urls import path
from userQueries.views import application_for_registration

app_name = 'userQueries'

urlpatterns = [
   path('application_registration/', application_for_registration, name="application_registration"),
]
