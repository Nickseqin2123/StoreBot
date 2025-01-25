from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from mainstore.maindb import Model, str128, str_256


class User(Model):
    __tablename__ = 'user'
    
    id: Mapped[str_256] = mapped_column(primary_key=True) 

    card = relationship('Card', back_populates='user', lazy='selectin') # ПРИМЕР: Если ты делаешь relationship для класса А из класса Б, то в классе Б дожен быть relationship для класса А


class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str_256] = mapped_column(unique=True)
    description: Mapped[str128]
    price: Mapped[float]
    count: Mapped[int]

    card = relationship('Card', back_populates='product', lazy='selectin')


class Card(Model):
    __tablename__ = 'card'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str_256] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    count: Mapped[int]

    product = relationship('Product', back_populates='card', lazy='selectin')
    user = relationship('User', back_populates='card', lazy='selectin')
    
    __table_args__ = (
        UniqueConstraint('user_id', 'product_id', name='uix_user_product'), # Комбинация user_id product_id, будет уникальной
    )