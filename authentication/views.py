from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from bookshop import settings

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/catalog')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',
        {'form': form})

@login_required
def logout_user(request):
    data = request.session.get('cart', None)
    logout(request)
    session = request.session
    if data:
        session[settings.CART_SESSION_ID] = data
        session.modified = True
    return redirect('home')