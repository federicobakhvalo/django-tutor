from urllib.parse import urlparse

from django import forms
import re

from django.db import transaction

from .models import Book,Reader,BookLoan
from .models_utils.mixins import TailwindFormMixin




class ReaderForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['first_name', 'last_name', 'email', 'phone','cover_url']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'cover_url':"Ссылка на фото (URL формат)"
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7XXXXXXXXXX или 8XXXXXXXXXX'
            }),
            'cover_url': forms.URLInput(attrs={'placeholder': 'Ссылка на автарку читателя'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone',None)
        if not phone:
            return phone
        phone = phone.strip()
        phone_regex = r'^(\+7|8)\d{10}$'
        if not re.match(phone_regex, phone):
            raise forms.ValidationError(
                'Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX'
            )

        return phone

class BookForm(TailwindFormMixin,forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
        labels = {
            'author': 'Автор',
            'bookname': 'Название книги',
            'review':"Рецензия",
            'description': 'Описание',
            'cover_url': 'Ссылка на обложку (URL формат)',
            'amount': 'Количество',
        }
        widgets = {
            'author': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-700  text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'bookname': forms.TextInput(attrs={'placeholder': 'Название книги'}),
            'review': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Описание книги',

            }),
            'cover_url': forms.URLInput(attrs={'placeholder': 'Ссылка на обложку'}),
            'amount': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_cover_url(self):
        url = self.cleaned_data.get('cover_url', '').strip()
        allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
        path = urlparse(url).path.lower()
        if not path.endswith(allowed_extensions):
            raise forms.ValidationError("Ссылка должна быть на изображение формата JPG, PNG, GIF или WEBP.")
        return url



class BookLoanForm(TailwindFormMixin,forms.ModelForm):
    class Meta:
        model = BookLoan
        exclude = ['issued_at', 'returned_at']
        labels = {
            'book': 'Книга',
            'reader': 'Читатель',
            'librarian': "Библиотекарь",
            'due_date':"Дата срока возврата книги"
        }
        widgets = {
            'book': forms.Select(),
            'reader': forms.Select(),
            'librarian':forms.Select(),
            'due_date':forms.DateInput(attrs={'placeholder':"Дата возврата",'type':"date",})

        }

    def clean_book(self):
        book = self.cleaned_data['book']
        if book.amount <= 0:
            raise forms.ValidationError('Эта книга недоступна для выдачи')
        return book

    def save(self, commit=True):
        book = self.cleaned_data['book']
        with transaction.atomic():
            book.amount -= 1
            book.save()
            return super().save(commit=commit)


class BookLoanUpdateForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = BookLoan
        fields = ['returned_at', 'due_date']
        labels = {
            'due_date': "Дата срока возврата книги",
            'returned_at':"Дата возврата книги читателем",

        }
        widgets = {
            'due_date': forms.DateInput(attrs={
                'placeholder': "Дата возврата",
                'type': "date"
            }),
            'returned_at': forms.DateInput(attrs={
                'placeholder': "Дата возврата читателем",
                'type': "date"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._was_returned = self.instance.returned_at is not None

    def clean_returned_at(self):
        if self._was_returned:
            raise forms.ValidationError('Книга уже возвращена')
        return self.cleaned_data['returned_at']
    def save(self, commit=True):
        with transaction.atomic():
            obj = super().save(commit=False)
            if not self._was_returned and obj.returned_at:
                book = obj.book
                book.amount += 1
                book.save()
            if commit:
                obj.save()
        return obj

