import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from db import db

class Author(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, unique=True, nullable=False)
    surname = Column(String(64), nullable=True)
    is_deleted = Column(Boolean, default=False, server_default='false')

    quotes = relationship('Quotes', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name, surname=None):
        self.name = name
        self.surname = surname

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "quotes": [q.to_dict() for q in self.quotes.filter_by(is_deleted=False).all()]
        }

class Quotes(db.Model):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    text = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False, default=1, server_default='1')
    is_deleted = Column(Boolean, default=False, server_default='false')
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, author, text, rating=1):
        self.author = author
        self.text = text
        self.rating = max(1, min(5, rating))

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "author_id": self.author_id,
            "rating": self.rating,
            "created_at": self.created_at.strftime("%d.%m.%Y") # Формат dd.mm.yyyy
        }
