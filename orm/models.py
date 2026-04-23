from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db import db

class Author(db.Model):
    __tablename__ = 'authors'
    __table_args__ = {'comment': 'Таблица авторов'}

    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, unique=True, nullable=False)
    surname = Column(String(64), nullable=True) # Задание 4: Добавили фамилию

    quotes = relationship('Quotes', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name, surname=None):
        self.name = name
        self.surname = surname

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "quotes": [q.to_dict() for q in self.quotes.all()]
        }


class Quotes(db.Model):
    __tablename__ = 'quotes'
    __table_args__ = {'comment': 'Таблица цитат'}

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    text = Column(String(255), nullable=False)

    def __init__(self, author, text):
        self.author = author 
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id
        }