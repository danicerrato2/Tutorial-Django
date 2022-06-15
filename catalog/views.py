from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from orders.forms import CartAddBookForm

from .models import Book, Comment

def home(request):

    most_popular_books = Book.objects.order_by('score').reverse()[:5]
    last_books = Book.objects.order_by('date').reverse()[:5]

    context = {
        'most_popular_books' : most_popular_books,
        'last_books' : last_books,
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
        context['form'] = CartAddBookForm()

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