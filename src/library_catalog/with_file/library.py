import json

from src.library_catalog.with_file.models import Book

class BookRepository:

    objs = []

    def __init__(self):
        self.read_data()

    @classmethod
    def read_data(cls):
        cls.objs.clear()
        with open("src/library_catalog/with_file/books.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
            for book in data:
                res = [i for i in book.values()]
                cls.objs.append(Book(*res))
            return cls.objs

    @classmethod
    def search_book(cls, id):
        for book in cls.objs:
            if book.id == int(id):
                return book
        return None

    def get_book(self, id):
        return self.search_book(id)

    def add_data(self, data):
        # можно добавить валидацию на существующий индекс
        res = [i for i in data.values()]
        self.objs.append(Book(len(self.objs) + 1, *res))
        self.write_to_file()

    def update_data(self, id, nd):
        # можно добавить валидацию на существующий индекс
        book = self.search_book(id)
        for key, value in nd.items():
            setattr(book, key, value)
        self.write_to_file()
        return book


    def delete_data(self, id):
        book = self.search_book(id)
        self.objs.remove(book)
        self.write_to_file()

    @classmethod
    def write_to_file(self):
        write_data = [i.__dict__ for i in self.objs]
        with open("src/library_catalog/with_file/books.json", "w", encoding="UTF-8") as file:
            json.dump(write_data, file,  ensure_ascii=False, indent=4)