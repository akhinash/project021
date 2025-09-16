from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    contact_info = models.CharField(max_length=100)

class BookShelf(models.Model):
    name = models.CharField(max_length=100)
    library = models.ForeignKey(Library, related_name='shelves', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('name', 'library')

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Book(models.Model):
    name = models.CharField(max_length=200)
    shelf = models.ForeignKey(BookShelf, related_name='books', on_delete=models.CASCADE)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('name', 'publisher', 'shelf')
