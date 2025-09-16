from rest_framework import serializers
from .models import Library, BookShelf, Author, Book

class LibrarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Library
        fields = '__all__'

    def validate_name(self, value):
        qs = Library.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Library with this name already exists.")
        return value


class BookShelfSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = BookShelf
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name') or (self.instance.name if self.instance else '')
        library = attrs.get('library') or (self.instance.library if self.instance else None)

        if not Library.objects.exists():
            raise serializers.ValidationError("Cannot create bookshelf because no Library exists.")

        if not library:
            raise serializers.ValidationError("BookShelf must be linked to a valid Library.")

        if not name or not name.strip():
            raise serializers.ValidationError("Shelf name cannot be empty.")

        qs = BookShelf.objects.filter(library=library, name__iexact=name)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Shelf name duplicated within the same Library.")
        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)
    class Meta:
        model = Book
        fields = ['id','name','publisher','shelf','authors','created_at']

    def validate(self, attrs):
        # pick values from attrs or instance (for updates)
        name = attrs.get('name') or (self.instance.name if self.instance else None)
        publisher = attrs.get('publisher') or (self.instance.publisher if self.instance else None)
        shelf = attrs.get('shelf') or (self.instance.shelf if self.instance else None)
        authors = attrs.get('authors') if 'authors' in attrs else (list(self.instance.authors.all()) if self.instance else [])

        if not shelf:
            raise serializers.ValidationError("Book must be linked to a valid BookShelf.")

        # Duplicate detection: same name + publisher + same set of authors
        candidate_qs = Book.objects.filter(name__iexact=name, publisher__iexact=publisher)
        if self.instance:
            candidate_qs = candidate_qs.exclude(pk=self.instance.pk)

        authors_set = set([a.pk for a in authors])

        for book in candidate_qs:
            book_author_set = set(book.authors.values_list('pk', flat=True))
            if book_author_set == authors_set:
                raise serializers.ValidationError("A book with the same name, publisher and authors already exists.")
        return attrs

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        book = Book.objects.create(**validated_data)
        book.authors.set(authors)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        for k,v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if authors is not None:
            instance.authors.set(authors)
        return instance
