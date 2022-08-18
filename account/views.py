from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

from .forms import UserForm

User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/survey')
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})
