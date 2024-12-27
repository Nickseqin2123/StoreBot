import asyncio

from sqlalchemy.ext.asyncio.session import async_sessionmaker
from models.models import User
from mainstore.maindb import cfg


async def work():
    session = async_sessionmaker(cfg.engine)
    
    try:

        async with session() as session:
            user = await session.get(User, ident=12312414)
            print(user.card)
            
    finally:
        await cfg.engine.dispose()


asyncio.run(work())
