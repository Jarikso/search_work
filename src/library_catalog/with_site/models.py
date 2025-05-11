from pydantic import BaseModel

class Book(BaseModel):
    id: int
    name: str
    author: str
    year: int
    genre: str
    pages: int
    availability: str

    def to_dict(self):
        return self.dict()