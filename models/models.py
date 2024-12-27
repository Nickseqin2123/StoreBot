from typing import Optional


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from mainstore.maindb import Model, str64, str_256


class User(Model):
    __tablename__ = 'user'
    
    id: Mapped[str_256] = mapped_column(primary_key=True) 

    card = relationship('Card', back_populates='user') # ПРИМЕР: Если ты делаешь relationship для класса А из класса Б, то в классе Б дожен быть relationship для класса А


class Products(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_256]
    description: Mapped[str64]
    price: Mapped[float]
    count: Mapped[int]

    card = relationship('Card', back_populates='products')


class Card(Model):
    __tablename__ = 'card'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str_256] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))

    products = relationship('Products', back_populates='card')
    user = relationship('User', back_populates='card')
