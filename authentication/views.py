from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import SignUpForm
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            """user = User.objects.create_user(username=request['username'],
                       password=request['password'],
                       first_name=request['first_name'],
                       last_name=request['last_name'],
                       email=request['email'])
            user.save()"""
            login(request, user)
            return redirect('/catalog')
    else:
        form = SignUpForm()
    return render(request, 'signup.html',
        {'form': form})
