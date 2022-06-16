from math import floor
from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from catalog.forms import VoteABookForm
from orders.forms import CartAddBookForm
from .models import Book, Comment, Vote
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

def home(request):

    most_popular_books = Book.objects.order_by('score').reverse()[:5]
    last_books = Book.objects.order_by('date').reverse()[:5]
    most_voted_books = Book.objects.order_by('num_votes').reverse()[:5]

    context = {
        'most_popular_books' : most_popular_books,
        'last_books' : last_books,
        'most_voted_books' : most_voted_books,
    }

    return render(request, 'home.html', context=context)

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)

        context['pk'] = self.kwargs.get('slug')
        book = Book.objects.get(slug=context['pk'])
        comments = Comment.objects.all().filter(book=book)
        context['comments'] = comments
        context['cart_form'] = CartAddBookForm()
        context['vote_form'] = VoteABookForm()

        return context

class SearchView(generic.ListView):
    model = Book
    template_name = 'catalog/search.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(Q(title__icontains=query)
            | Q(author__last_name__icontains=query)
            | Q(author__first_name__icontains=query)).distinct()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query_search'] = query
        return context

@login_required
@require_POST
def vote(request, slug):
    """ add the book with slug " book_slug " to the
    shopping cart . The number of copies to be bought
    may be obtained from the form CartAddBookForm """
    book = Book.objects.all().get(slug=slug)
    form = VoteABookForm(request.POST)
    user = request.user

    if form.is_valid():
        score = form.cleaned_data['score']
        vote = Vote(score=score, book=book, user=user)
        vote.save()

    return redirect('home')