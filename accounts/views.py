from django.shortcuts import render,redirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView
from .forms import SignUpForm,LoginForm
from django.contrib.auth import login,authenticate

class SignupPageView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username = username, password = password)

        if user is not None:
            login(self.request, user)
        
        return redirect(self.success_url)

class LoginPageView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    next_page = '/'
