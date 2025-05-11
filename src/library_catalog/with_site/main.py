from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
import requests

from src.library_catalog.with_site.models import Book

JSONBIN_API_KEY = "$2a$10$05U0e8DEmRLkv/bBlY/jMuYVg/.ZE0Iw.MW60BB72qY8pLo5hHTAK"
JSONBIN_URL = "https://api.jsonbin.io/v3/b/681cfb678561e97a50101676"
headers = {"X-Master-Key": JSONBIN_API_KEY, "Content-Type": "application/json"}
app = FastAPI()



def get_books():
    response = requests.get(JSONBIN_URL + "/latest", headers=headers)
    if response.status_code == 200:
        return response.json().get("record", [])
    return []

all_books = get_books()


def search_book(idb):
    for i in all_books:
        if i['id'] == int(idb):
            return i

def save_books() -> bool:
    response = requests.put(JSONBIN_URL, json=all_books, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error saving books")
    return True

@app.get("/books/", response_model=list[Book])
def get_books():
    return all_books


@app.get("/book/{id}", response_model=Book)
def get_book(id: str):
    return search_book(id)


@app.post("/books/", response_model=Book)
def add_book(book: dict = Body()):
    new_book = Book(
        id=len(all_books),
        name=book["name"],
        author=book["author"],
        year=book["year"],
        genre=book["genre"],
        pages=book["pages"],
        availability=book.get("availability", "available")
    )
    book_dict = jsonable_encoder(new_book)
    all_books.append(book_dict)
    save_books()
    return new_book

@app.put("/book/{book_id}", response_model=Book)
def update_book(book_id: int, data: dict = Body()):

    book = search_book(book_id)
    for key, value in data.items():
        book[key] = value
    save_books()
    return book

@app.delete("/book/{id}", response_model=Book)
def delete_book(id: int):
    book = search_book(id)
    all_books.pop(all_books.index(book))
    save_books()
    return book