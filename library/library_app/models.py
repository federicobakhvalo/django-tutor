from django.db import models

from .models_utils.enums import BookStatus


# Create your models here.


class BookAuthor(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    bio = models.TextField(max_length=10000, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(BookAuthor, on_delete=models.CASCADE, related_name='books')
    bookname = models.CharField(max_length=100)
    review = models.TextField(null=True, blank=True, max_length=1000)
    amount = models.PositiveIntegerField(default=0)
    cover_url = models.URLField(max_length=1000)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'bookname'],
                name='unique_book_per_author'
            )
        ]

    def __str__(self):
        return f'{self.bookname} - {self.author}'


class Reader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    cover_url=models.URLField(max_length=1000,null=True,blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Librarian(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cover_url=models.URLField(max_length=1000,null=True,blank=True)
    hired_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class BookLoan(models.Model):
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    librarian = models.ForeignKey(
        Librarian,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_loans'
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'reader'],
                condition=models.Q(returned_at__isnull=True),
                name='unique_active_bookloan'
            )
        ]

    def __str__(self):
        return f'{self.book} → {self.reader}'
