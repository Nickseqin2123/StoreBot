from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine


class Model(DeclarativeBase):
    ...


class Configurator:
    __USERNAME: str = 'root'
    __PASSWORD: str = 'ZXCPUDGE228NEKITvip123'
    __HOST: str = '127.0.0.1'
    __DB_NAME: str = 'store'
    __PORT: int = 3306


    def __init__(self, type_connect: str = 'async'):
        connectors = {
            'async': create_async_engine(self.async_connect_url),
            'sync': create_engine(self.sync)
        }

        self.engine = connectors[type_connect]

    @property
    def async_connect_url(self):
        return f'mysql+aiomysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'
    
    @property
    def sync(self):
        return f'mysql+pymysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'


con = Configurator()
print(con.sync)
