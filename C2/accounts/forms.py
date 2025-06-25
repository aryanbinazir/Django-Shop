from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForms(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirmation password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number', 'email',  'full_name']

    def phone_number_start_0(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('0'):
            raise ValueError('Number should starts with zero(like:09121234567)')
        return phone_number

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and ['password1'] != ['password2']:
            raise ValidationError('Passwords must be match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change password with <a href=\'../password/\'>this form</a>')

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name','password', 'last_login', 'is_active', 'is_admin')

class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    full_name = forms.CharField()
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email has already exist')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This number has already exist')
        return phone_number

class UserVerifyCodeForm(forms.Form):
    code = forms.IntegerField()

class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)


