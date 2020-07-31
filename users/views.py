from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import AuthenticationForm
from users.forms import CustomUserCreationForm, CustomUserLoginForm
from django.http import HttpResponse


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f'user: {user}')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('home')

def login_request(request):
    if request.method == 'POST':
        form = CustomUserLoginForm()
        print(form)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            if user is not None:
                print(f'Logged in as {email}.')
                login(request, user)
                return redirect('home')
            else:
                print('Invalid username or password.')
        else:
            print("Invalid form")
    form = CustomUserLoginForm()
    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
    )
