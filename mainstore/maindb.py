from typing import Annotated
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import create_engine, String


str_256 = Annotated[str, 256]
str64 = Annotated[str, 64]


class Model(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str64: String(64)
    }
    


class Configurator:
    __USERNAME: str = 'root'
    __PASSWORD: str = 'ZXCPUDGE228'
    __HOST: str = '127.0.0.1'
    __DB_NAME: str = 'store'

    def __init__(self, type_connect: str = 'async'):
        connectors = {
            'async': create_async_engine(self.async_connect_url),
            'sync': create_engine(self.sync)
        }

        self.engine: AsyncEngine = connectors[type_connect]
        
    @property
    def async_connect_url(self):
        return f'mysql+aiomysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'
    
    @property
    def sync(self):
        return f'mysql+pymysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'


cfg = Configurator()