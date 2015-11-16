from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy import create_engine
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    title = Column(String(80), nullable=False)
    description = Column(String(250))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    category = relationship(Category)
    filename = Column(String(80), nullable=True)

    @property
    def serialize(self):
        return{
            'cat_id': self.category_id,
            'description': self.description,
            'id': self.id,
            'title': self.title
        }


engine = create_engine('postgresql:///itemcatalog')
Base.metadata.create_all(engine)


