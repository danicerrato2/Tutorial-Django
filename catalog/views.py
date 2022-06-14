from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db.models import Q

from .models import Book

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

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html',
                      context={'book': book})

class SearchView(generic.ListView):
    model = Book
    template_name = 'search.html'
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