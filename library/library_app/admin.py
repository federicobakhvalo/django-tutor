from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(BookLoan)
admin.site.register(Librarian)
admin.site.register(BookAuthor)

