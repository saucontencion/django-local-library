from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
# def index(request):
#     return render(request, 'catalogo/index.html')

class GenreListView(ListView):
    model = Genre
    template_name = 'catalogo/genre_list.html'

class GenreDetailView(DetailView):
    model = Genre
    template_name = 'catalogo/genre_detail.html'

from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

     # Calcular el número de géneros
    num_genres = Genre.objects.count()

    # Calcular el número de libros que contienen una palabra específica (case-insensitive)
    search_word = request.GET.get('search_word', '')  # Obtener la palabra de búsqueda del parámetro GET
    num_books_containing_word = Book.objects.filter(title__icontains=search_word).count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_containing_word': num_books_containing_word,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author



class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalogo/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
