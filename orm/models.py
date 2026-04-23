from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func, Boolean
from db import db

class Quotes(db.Model):
    __tablename__ = 'quotes'
    __table_args__ = {
        'comment': u'Таблица с цитатами'
    }

    id = Column(Integer, primary_key=True, comment='Идентификатор цитаты')
    author = Column(String(100), nullable=False, comment='Автор цитаты')
    text = Column(String(255), nullable=False, comment='Текст цитаты')
    rating = Column(Integer, default=1, comment='Рейтинг (1-5 звезд)')

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "rating": self.rating
        }