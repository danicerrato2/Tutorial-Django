from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Book
from .forms import CartAddBookForm
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def cart_add(request, book_slug):
    """ add the book with slug " book_slug " to the
    shopping cart . The number of copies to be bought
    may be obtained from the form CartAddBookForm """
    cart = Cart(request)

    form = CartAddBookForm(request.POST)
    if form.is_valid():
        book = get_object_or_404(Book, slug=book_slug)
        units = form.cleaned_data['units']
    
    cart.add(book, units)
    return redirect('cart_list')

@login_required
def cart_list(request):
    return render(request, 'orders/cart_list.html',
        context={'cart': Cart(request)})