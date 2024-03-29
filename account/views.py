from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View

from django_login_history.models import Login

from account.forms import AccountAuthenticationForm, RegistrationForm

from division.models import Division
from document.models import DocSKAI
from .models import Account

class LoginHistory(LoginRequiredMixin, View):
    def get(self, request):
        context = {}

        context["login"] = Login.objects.all().order_by('-date')

        return render(request, 'account/login_history.html', context)

class DashboardView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context = {}
        
        count_account = Account.objects.count()
        count_skai = DocSKAI.objects.count()


        context["count_account"] = count_account
        context["count_skai"] = count_skai

        # profile = request.user
        # admin = Account.objects.get(pk=1)
        # profile.create_notif_first_login(admin)

        return render(request, 'account/dashboard.html', context)

def dashboard_view(request,*args,**kwargs):
    return render(request, 'account/dashboard.html', {})

def login_view(request,*args,**kwargs):
    context = {}

    division = Division.objects.all()
    context["divisions"] = division

    user = request.user
    if user.is_authenticated: 
        return redirect("home")
        
    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST and 'login' in request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            print(user)
            if user.is_admin == True or user.is_staff == True or user.is_active == True:
                login(request, user)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            form = AccountAuthenticationForm()
            print("Not Valid")
            
        context['login_form'] = form
    
    if request.POST and 'regis' in request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            email = form.cleaned_data.get('email').lower()
            #raw_password = form.cleaned_data.get('pwd1')
            
            #account = authenticate(email=email, password=raw_password)
            login(request, account)
            
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            print(form.error_messages)
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/login.html', context)

def logout_view(request,*args,**kwargs):
    logout(request)
    return redirect("home")

def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect