from django import forms
from userQueries.models import ApplicationForRegistration


class ApplicationForRegistrationForm(forms.ModelForm):
   """Форма заявки для регистрации пользователей"""
   email = forms.EmailField(required=True)

   class Meta:
      model = ApplicationForRegistration
      fields = ['email', 'phone']

   def save(self, commit=True):
      application = super(ApplicationForRegistrationForm, self).save(commit=False)
      application.email = self.cleaned_data['email']
      application.phone = self.cleaned_data['phone']
      if commit:
         application.save()
      return True
