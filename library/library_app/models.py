from django.db import models


# Create your models here.


class BookAuthor(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    bio = models.TextField(max_length=10000, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name







