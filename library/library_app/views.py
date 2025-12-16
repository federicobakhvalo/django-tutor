from django.db.models import F, Q
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView,ListView
from .models import *
from .forms import *
from django.db import transaction

# Create your views here.


class MainPageView(TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = [
            {'title': 'Все книги', 'url': '/books/'},
            {'title': 'Предложить книгу', 'url': '/create_book/'},
            {'title': 'Создать читателя', 'url': '/create_reader/'},
            {'title': 'Выдача книг', 'url': '/book_loan_history/'},
        ]
        return context


class CreateBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'forms/form.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Предложить книгу'
        return context
#


class CreateReaderView(CreateView):
    model=Reader
    form_class = ReaderForm
    template_name = 'forms/form.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать читателя'
        return context


class CreateBookLoan(CreateView):
    model=BookLoan
    template_name = 'forms/form.html'
    form_class = BookLoanForm
    success_url = reverse_lazy('main')

    def get_initial(self):
        initial = super().get_initial()
        book_id = self.request.GET.get('book_to')
        if book_id:
            initial['book'] = book_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Забронировать книгу'
        return context



class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Book.objects
            .select_related('author')
            .annotate(author_name=F('author__name'))
        )
        self.q = self.request.GET.get('q', '').strip()
        if self.q:
            queryset = queryset.filter(Q(bookname__icontains=self.q) | Q(author_name__icontains = self.q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.q
        return context


class BookLoanListView(ListView):
    model = BookLoan
    template_name = 'books/book_loan.html'
    context_object_name = 'loans'
    paginate_by = 10

    def get_queryset(self):
        queryset = BookLoan.objects.select_related('book', 'reader', 'librarian')
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(book__bookname__icontains=q) |
                Q(reader__first_name__icontains=q) |
                Q(reader__last_name__icontains=q)
            )
        queryset = queryset.order_by('-issued_at')
        return queryset