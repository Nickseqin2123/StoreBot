import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, delete, update, select
from models.models import User, Card, Product
from mainstore.maindb import cfg


def getUser(func):
    
    async def wrapper(*args, **kwargs):
        session = async_sessionmaker(cfg.engine)
        
        try:

            async with session() as session:
                user = await session.get(User, ident=kwargs['user_id'])
                
                if not user:
                    return await func(**kwargs)
                
                return f'Пользователь {user.id} уже есть в базе'
        finally:
            await cfg.engine.dispose()
    
    return wrapper


def checkUserCard(func):
    
    async def wrapper(*args, **kwargs):
        session = async_sessionmaker(cfg.engine)
        
        try:
            async with session() as session:
                query = select(Card).filter(Card.user_id == kwargs['user_id'])
                resp = await session.execute(query)
                
                res = resp.first()
                if res:
                    return await func(**kwargs)
                
    
                    
        finally:
            await cfg.engine.dispose()

    
    return wrapper


@getUser
async def addUser(user_id: int): # В связке с get_user. Подаем четкие аргументы(только kwargs см. в get_user)
    '''
    Добавляет пользователя в бд, если его там нет.
    Работает с декоратором get_user
    '''
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        query = insert(User).values(id=user_id)
            
        await session.execute(query)
        await session.commit()
        
    return f'Пользователь {user_id} добавлен в базу'
    

async def deleteProductUser(user_id: int, product_id: int, count: int):
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        async with session.begin():
            
            query_delete = delete(Card).filter(Card.user_id == user_id, Card.product_id == product_id)
            await session.execute(query_delete)
            
            query_add = update(Product).filter(Product.id == product_id).values(count=Product.count + count)
            await session.execute(query_add)
    
    return 'Удаление прошло успешно'
    

@checkUserCard
async def subUserCountCard(user_id: int, product_id: int, count_change: int):
    session = async_sessionmaker(cfg.engine)
    

    async with session() as session:
        async with session.begin():
            user_tovar = select(Card).filter(Card.user_id == user_id, Card.product_id == product_id)
            user_tovar = await session.execute(user_tovar)
            
            count_in_base = user_tovar.scalar_one_or_none()
                    
            if count_change >= count_in_base.count:
                await deleteProductUser(user_id=user_id, product_id=product_id, count=count_in_base)
            
            query_sub_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count - count_change)
            await session.execute(query_sub_user)
            
            query_add_product = update(Product).filter(Product.id == product_id).values(count=Product.count + count_change)       
            await session.execute(query_add_product)

                                
    return 'Кол-во товара было уменьшено у вас в корзине успешно'
    
    
@checkUserCard
async def addProductCountUserCard(user_id: int, product_id: int, count_change: int):
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        async with session.begin():
            product = select(Product).filter(Product.id == product_id)
            resp = await session.execute(product)
            count_in_base_product = resp.scalar_one().count
            
            if count_change > count_in_base_product:
                return 'На складе нет столько товара!'
            
            query_sub_sklad = update(Product).filter(Product.id == product_id).values(count=Product.count - count_change)
            await session.execute(query_sub_sklad)
                
            query_add_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count + count_change)
            res = await session.execute(query_add_user)
            
            if res.rowcount == 0:
                card_user = insert(Card).values(user_id=user_id, product_id=product_id, count=count_change)
                await session.execute(card_user)
                
        await session.commit()
    
    return 'Добавление товара прошло успешно'


@checkUserCard
async def getUserCard(user_id: int):
    session = async_sessionmaker(cfg.engine)
    
    async with session() as session:
        query = select(Card).filter(Card.user_id == user_id)
        return_rows = await session.execute(query)
            
        return return_rows.all()


async def getProducts():
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            query = select(Product)
            response = await session.execute(query)
            selects = response.all()
            
            if selects:
                return selects
            return 'На складе нет товаров ;<'
            
    finally:
        await cfg.engine.dispose()