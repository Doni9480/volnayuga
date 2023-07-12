from django import forms
from userQueries.models import ApplicationForRegistration, Feedback


class ApplicationForRegistrationForm(forms.ModelForm):
   """Форма заявки для регистрации пользователей"""
   email = forms.EmailField(required=True)

   class Meta:
      model = ApplicationForRegistration
      fields = ['name', 'email', 'phone']

   def save(self, commit=True):
      application = super(ApplicationForRegistrationForm, self).save(commit=False)
      application.name = self.cleaned_data['name']
      application.email = self.cleaned_data['email']
      application.phone = self.cleaned_data['phone']
      if commit:
         application.save()
      return True


class FeedbackForm(forms.ModelForm):
   name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Ваше имя", 'id': "id_username_feedback"}))
   phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': "Ваш телефон", 'class': "phone-maske", 'id': "id_phone_feedback"}))
   email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': "Ваш E-mail", 'id': "id_email_feedback"}))
   message = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': "Ваше сообщение", 'rows':"1", 'id': "id_message_feedback"}))

   class Meta:
      model = Feedback
      fields = ['name', 'phone', 'email', 'message']

   def save(self, commit=True):
      obj = super(FeedbackForm, self).save(commit=False)
      obj.name = self.cleaned_data['name']
      obj.phone = self.cleaned_data['phone']
      obj.email = self.cleaned_data['email']
      obj.message = self.cleaned_data['message']
      if commit:
         obj.save()
      return True