import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, update, select, delete
from mainstore.maindb import cfg
from models.models import Product


async def addProduct(product_id: int, count_change: int, name: str = None, price: str = None, description: str = 'Без описания'):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            async with session.begin():
                query = update(Product).filter(Product.id == product_id).values(count=Product.count + count_change)
                info = await session.execute(query)
                
                if info.rowcount == 0:
                    add_product = insert(Product).values(name=name, price=price, description=description, count=count_change)
                    await session.execute(add_product)
                    return 'Товар был добавлен на склад'
                    
    except Exception as er:
        print(er, end='\n')
        return 'Неожиданная ошибка, перезапустите бота. Отправьте /start'
    finally:
        await cfg.engine.dispose()
    return 'Склад пополнился'
    

async def subProduct(product_id: int, count_change: int):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            async with session.begin():
                user_tovar = select(Product).filter(Product.id == product_id)
                user_tovar = await session.execute(user_tovar)
                
                base = user_tovar.scalar_one_or_none()
                
                if count_change >= base.count:
                    query_delete = delete(Product).filter(Product.id == product_id)
                    await session.execute(query_delete)
                    
                    return 'Удаление прошло успешно'
                
                query_sub = update(Product).filter(Product.id == product_id).values(count=Product.count - count_change)
                await session.execute(query_sub)
    except Exception as er:
        print(er)
        return 'Неожиданная ошибка, перезапустите бота. Отправьте /start'
    finally:
        await cfg.engine.dispose()
    
    return 'Кол-во товара было уменьшено'


async def delete_product(product_id: int):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            async with session.begin():
                delet = delete(Product).filter(Product.id == product_id)
                await session.execute(delet)
    finally:
        await cfg.engine.dispose()
    
    return 'Удаление прошло успешно'