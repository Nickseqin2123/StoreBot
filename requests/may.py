import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy import insert, delete
from models.models import User, Card
from mainstore.maindb import cfg


def get_user(func):
    
    async def wrapper(*args, **kwargs):
        session = async_sessionmaker(cfg.engine)
        
        try:

            async with session() as session:
                user = await session.get(User, ident=kwargs['user_id'])
                
                if not user:
                    await func(**kwargs)
                   
        finally:
            await cfg.engine.dispose()
    
    return wrapper


# @get_user
# async def add_user(user_id: int): # В связке с get_user. Подаем четкие аргументы(только kwargs см. в get_user)
#     session = async_sessionmaker(cfg.engine)
    
#     async with session() as session:
#         query = insert(User).values(id=user_id)
            
#         await session.execute(query)
#         await session.commit()
#         print('Nice!')
    

# asyncio.run(add_user(user_id=1231244))

# @get_user
# async def delete_product(user_id: int, product_id: int):
#     session = async_sessionmaker(cfg.engine)
    
#     try:
#         async with session() as session:
#             query = delete(Card).filter()
                
#     finally:
#         await cfg.engine.dispose()
    

