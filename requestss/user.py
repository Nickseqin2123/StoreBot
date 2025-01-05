import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, delete, update, select
from models.models import User, Card, Product
from mainstore.maindb import cfg


def get_user(func):
    
    async def wrapper(*args, **kwargs):
        session = async_sessionmaker(cfg.engine)
        
        try:

            async with session() as session:
                user = await session.get(User, ident=kwargs['user_id'])
                
                if not user:
                    await func(**kwargs)
                    return f'Пользователь {kwargs['user_id']} добавлен в базу'
                else:
                    return f'Пользователь {user.id} уже есть в базе'
        finally:
            await cfg.engine.dispose()
    
    return wrapper


def check_user_cart(func):
    
    async def wrapper(*args, **kwargs):
        session = async_sessionmaker(cfg.engine)
        
        try:
            async with session() as session:
                query = select(Card).filter(Card.user_id == kwargs['user_id'])
                resp = await session.execute(query)
                
                first_res = resp.first()[0]
                kwargs.update({'user_card': first_res})
                    
                if bool(first_res):
                    await func(**kwargs)
        finally:
            await cfg.engine.dispose()

    
    return wrapper


@get_user
async def add_user(user_id: int): # В связке с get_user. Подаем четкие аргументы(только kwargs см. в get_user)
    '''
    Добавляет пользователя в бд, если его там нет.
    Работает с декоратором get_user
    '''
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        query = insert(User).values(id=user_id)
            
        await session.execute(query)
        await session.commit()
    
    return 'Пользователь добавлен в базу'
    

async def delete_product_user(user_id: int, product_id: int, count: int):
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        async with session.begin():
            
            query_delete = delete(Card).filter(Card.user_id == user_id, Card.product_id == product_id)
            await session.execute(query_delete)
            
            query_add = update(Product).filter(Product.id == product_id).values(count=Product.count + count)
            await session.execute(query_add)
    
    return 'Операция прошла успешно'
    

@check_user_cart
async def sub_user_count_card(user_id: int, product_id: int, count_change: int, user_card: Card = None):
    session = async_sessionmaker(cfg.engine)
    

    async with session() as session:
        async with session.begin():
            
            count_in_base = user_card.count
                    
            if count_change >= count_in_base:
                await delete_product_user(user_id=user_id, product_id=product_id, count=count_in_base)
                
            # user_card.count -= count_change 
            query_sub_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count - count_change)
            await session.execute(query_sub_user)
            
            query_add_product = update(Product).filter(Product.id == product_id).values(count=Product.count + count_change)
            
            await session.execute(query_add_product)

                                
    return 'Операция прошла успешно'
    
    
@check_user_cart
async def add_product_count_user_card(user_id: int, product_id: int, count_change: int, user_card: Card = None):
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        async with session.begin():
            product = select(Product).filter(Product.id == product_id)
            resp = await session.execute(product)
            count_in_base_product = resp.first()[0].count
            
            if count_change > count_in_base_product:
                return 'На складе нет столько товара!'
            
            query_sub_sklad = update(Product).filter(Product.id == product_id).values(count=Product.count - count_change)
            await session.execute(query_sub_sklad)
                
            query_add_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count + count_change)
            await session.execute(query_add_user)
                
        await session.commit()


@check_user_cart
async def get_user_card(user_id, user_card: Card = None):
    print(user_card)


asyncio.run(sub_user_count_card(user_id=1124518724, product_id=1, count_change=1))


# Узнать насчет user_card параметра и user_card.count -= count_change 