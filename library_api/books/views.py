from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Library, BookShelf, Author, Book
from .serializers import LibrarySerializer, BookShelfSerializer, AuthorSerializer, BookSerializer

class LibraryListCreateUpdate(APIView):
    def get(self, request):
        qs = Library.objects.all()
        serializer = LibrarySerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        pk = data.get('id')
        if pk:
            try:
                instance = Library.objects.get(pk=pk)
            except Library.DoesNotExist:
                return Response({"detail":"Library not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = LibrarySerializer(instance, data=data)
        else:
            serializer = LibrarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibraryDetail(APIView):
    def get(self, request, pk):
        try:
            obj = Library.objects.get(pk=pk)
        except Library.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = LibrarySerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            obj = Library.objects.get(pk=pk)
        except Library.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookShelfListCreateUpdate(APIView):
    def get(self, request):
        qs = BookShelf.objects.all()
        serializer = BookShelfSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        pk = data.get('id')
        if pk:
            try:
                instance = BookShelf.objects.get(pk=pk)
            except BookShelf.DoesNotExist:
                return Response({"detail": "BookShelf not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookShelfSerializer(instance, data=data)
        else:
            serializer = BookShelfSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookShelfDetail(APIView):
    def get(self, request, pk):
        try:
            obj = BookShelf.objects.get(pk=pk)
        except BookShelf.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookShelfSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            obj = BookShelf.objects.get(pk=pk)
        except BookShelf.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorListCreateUpdate(APIView):
    def get(self, request):
        qs = Author.objects.all()
        serializer = AuthorSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        pk = data.get('id')
        if pk:
            try:
                instance = Author.objects.get(pk=pk)
            except Author.DoesNotExist:
                return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = AuthorSerializer(instance, data=data)
        else:
            serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetail(APIView):
    def get(self, request, pk):
        try:
            obj = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthorSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            obj = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookListCreateUpdate(APIView):
    def get(self, request):
        qs = Book.objects.all()

        # --- Search ---
        search = request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(shelf__name__icontains=search) |
                Q(authors__name__icontains=search)
            ).distinct()

        # --- Sorting ---
        ordering = request.GET.get('ordering')
        if ordering in ['name', 'date_created', 'authors__name']:
            qs = qs.order_by(ordering)

        # --- Filtering by author or publisher ---
        author = request.GET.get('author')
        if author:
            qs = qs.filter(authors__name__icontains=author)
        publisher = request.GET.get('publisher')
        if publisher:
            qs = qs.filter(publisher__icontains=publisher)

        # --- Pagination ---
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size
        total = qs.count()
        serializer = BookSerializer(qs[start:end], many=True)
        return Response({
            "count": total,
            "results": serializer.data
        })

    def post(self, request):
        data = request.data
        pk = data.get('id')
        if pk:
            try:
                instance = Book.objects.get(pk=pk)
            except Book.DoesNotExist:
                return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = BookSerializer(instance, data=data)
        else:
            serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    def get(self, request, pk):
        try:
            obj = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(obj)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            obj = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

