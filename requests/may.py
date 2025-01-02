import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, delete, update, select
from models.models import User, Card, Product
from mainstore.maindb import cfg


# def get_user(func):
    
#     async def wrapper(*args, **kwargs):
#         session = async_sessionmaker(cfg.engine)
        
#         try:

#             async with session() as session:
#                 user = await session.get(User, ident=kwargs['user_id'])
                
#                 if not user:
#                     await func(**kwargs)
                   
#         finally:
#             await cfg.engine.dispose()
    
#     return wrapper


# def check_user_cart(func):
    
#     async def wrapper(*args, **kwargs):
#         session = async_sessionmaker(cfg.engine)
        
#         try:
#             async with session() as session:
#                 query = select(Card).filter(Card.user_id == kwargs['user_id'])
#                 resp = await session.execute(query)
                    
#                 if bool(resp.first()):
#                     await func(**kwargs)
#         finally:
#             await cfg.engine.dispose()

    
#     return wrapper


# @get_user
# async def add_user(user_id: int): # В связке с get_user. Подаем четкие аргументы(только kwargs см. в get_user)
#     session = async_sessionmaker(cfg.engine)
    
#     async with session() as session:
#         query = insert(User).values(id=user_id)
            
#         await session.execute(query)
#         await session.commit()
    
#     return 'Пользователь добавлен в базу'
    

# asyncio.run(add_user(user_id=12312414))


# async def delete_product_user(user_id: int, product_id: int, count: int):
#     session = async_sessionmaker(cfg.engine)
    
#     async with session() as session:
#         async with session.begin():
            
#             query_delete = delete(Card).filter(Card.user_id == user_id, Card.product_id == product_id)
#             await session.execute(query_delete)
            
#             query_add = update(Product).filter(Product.id == product_id).values(count=Product.count + count)
#             await session.execute(query_add)
    
#     return 'Операция прошла успешно'
    

# @check_user_cart
# async def sub_user_count_card(user_id: int, product_id: int, count_change: int):
#     session = async_sessionmaker(cfg.engine)
    

#     async with session() as session:
#         async with session.begin():
#             user_card = select(Card).filter(Card.user_id == user_id, Card.product_id == product_id)
#             resp = await session.execute(user_card)
#             count_in_base = resp.first()[0].count
                    
#             if count_change >= count_in_base:
#                 await delete_product_user(user_id=user_id, product_id=product_id, count=count_in_base)
                
                
#             query_sub_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count - count_change)
#             await session.execute(query_sub_user)
                        
#             query_add_product = update(Product).filter(Product.id == product_id).values(count=Product.count + count_change)
#             await session.execute(query_add_product)

                                
#     return 'Операция прошла успешно'


# asyncio.run(sub_user_count_card(user_id=12312414, product_id=1, count_change=5))
    
    
# @check_user_cart
# async def add_product_count_user_card(user_id: int, product_id: int, count_change: int):
#     session = async_sessionmaker(cfg.engine)
    
#     async with session() as session:
#         async with session.begin():
#             product = select(Product).filter(Product.id == product_id)
#             resp = await session.execute(product)
#             count_in_base_product = resp.first()[0].count
            
#             if count_change > count_in_base_product:
#                 return 'На складе нет столько товара!'
            
#             query_sub_sklad = update(Product).filter(Product.id == product_id).values(count=Product.count - count_change)
#             await session.execute(query_sub_sklad)
                
#             query_add_user = update(Card).filter(Card.user_id == user_id, Card.product_id == product_id).values(count=Card.count + count_change)
#             await session.execute(query_add_user)
                
#         await session.commit()


# print(asyncio.run(add_product_count_user_card(user_id=12312414, product_id=1, count_change=20)))