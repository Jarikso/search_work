from fastapi import FastAPI, Response, Body

from .library import BookRepository


app = FastAPI()

books = BookRepository()

@app.get("/books")
def get_books():
    return books.read_data()

@app.get("/book/{id}")
def get_book(id):
    return books.get_book(id)


@app.post("/books")
def add_book(data = Body()):
    books.add_data(data)
    return "Книга успешно добавлена"

@app.put("/book/{id}")
def update_book(id, data = Body()):
    return books.update_data(id, data)

@app.delete("/book/{id}")
def delete_book(id):
    # обработка чарез метод класс BookRepository delete
    books.delete_data(id)
    return "Данные успешно удалены"
