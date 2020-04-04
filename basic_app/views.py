from django.shortcuts import render
from .forms import UserPofileInfoForm,UserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate


# Create your views here.
def index(request):
    return  render(request,'basic_app/basep}.html')


@login_required
def special(request):
    return HttpResponse("you are logged in, nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))







def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserPofileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pics' in request.FILES:
                profile.profile_pic = request.FILES['profile_pics']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserPofileInfoForm()

    # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    return render(request,'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered,})

def user_login(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('basic_app:index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("someone tried login")
            print("Username {} and password {}".format(username,password))
            return HttpResponse("invalid login details")
    else:
        return render(request,'basic_app/login.html',{})





