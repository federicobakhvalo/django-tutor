from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('',MainPageView.as_view(),name='main'),
    path('create_book/',CreateBookView.as_view(),name='create_book'),
    path('create_reader/',CreateReaderView.as_view(),name='create_reader'),
    path('books/',BookListView.as_view(),name='books'),
    path('create_book_loan/',CreateBookLoan.as_view(),name='create_book_loan'),
    path('book_loan_history/',BookLoanListView.as_view(),name='book_loan_history')
]
