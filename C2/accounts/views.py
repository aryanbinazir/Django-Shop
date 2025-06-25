from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, UserVerifyCodeForm, UserLoginForm
from .models import User, OtpCode
#from uttils import sms_otp_code
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_class = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_class, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = OtpCode.objects.filter(phone_number=cd['phone_number'])
            if code_instance.exists():
                code_instance.delete()
            random_code = random.randint(1000, 10000)
            #sms_otp_code(phone_number=cd['phone_number'], code=random_code)
            OtpCode.objects.create(phone_number=cd['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': cd['phone_number'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password']
            }
            print(random_code)
            messages.success(request, 'I sent you a message', 'success')
            return redirect('accounts:user_register_verify_code')
        return render(request, self.template_class, {'form': form})

class UserRegisterVerifyCodeView(View):
    form_class = UserVerifyCodeForm
    template_class = 'accounts/register_verify.html'

    def get(self, request):
        return render(request, self.template_class, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_registration_info']
        code_instance = get_object_or_404(OtpCode, phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if code_instance.is_expired():
                    code_instance.delete()
                    messages.warning(request, 'This code has expired.Please try again.', 'warning')
                    return redirect('accounts:user_register')
                User.objects.create_user(
                    phone_number= user_session['phone_number'],
                    email= user_session['email'],
                    full_name= user_session['full_name'],
                    password= user_session['password']
                )
                code_instance.delete()
                messages.success(request, 'User registered successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Code is wrong', 'warning')
            return render(request, self.template_class, {'form': form})
        return render(request, self.template_class, {'form': form})
class UserLoginView(View):
    form_class = UserLoginForm
    template_class = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_class, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code_instance = OtpCode.objects.filter(phone_number=cd['phone_number'])
            if code_instance.exists():
                code_instance.delete()
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                verify_code = random.randint(1000,10000)
                OtpCode.objects.create(phone_number=cd['phone_number'], code=verify_code)
                #sms_otp_code(phone_number=cd['phone_number'], code=verify_code)
                request.session['user_login_info'] = {
                    'phone_number': cd['phone_number'],
                    'password': cd['password']
                }
                print(verify_code)
                messages.success(request, 'We sent you a code', 'success')
                return redirect('accounts:user_login_verify_code')
            messages.warning(request, 'username or password is not correct', 'warning')
            return render(request, self.template_class, {'form': form})
        return render(request, self.template_class, {'form': form})

class UserLoginVerifyCodeView(View):
    form_class = UserVerifyCodeForm
    template_class = 'accounts/login_verify.html'

    def get(self, request):
        return render(request, self.template_class, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_login_info']
        code_instance = get_object_or_404(OtpCode, phone_number=user_session['phone_number'])
        user = get_object_or_404(User, phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd['code']:
                if code_instance.is_expired():
                    code_instance.delete()
                    messages.warning(request, 'This code has expired.Please try again.', 'warning')
                    return redirect('accounts:user_login')
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'Code is wrong', 'warning')
            return render(request, self.template_class, {'form': form})
        return render(request, self.template_class, {'form': form})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out:)', 'success')
        return redirect('home:home')

class UserPasswordResetView(auth_views.PasswordResetView):
    users_email = User.objects.all()
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'
class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'












