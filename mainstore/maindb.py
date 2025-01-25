import configparser

from typing import Annotated
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import create_engine, String


str_256 = Annotated[str, 256]
str128 = Annotated[str, 128]


class Model(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str128: String(128)
    }
    

class Configurator:
    __USERNAME: str = ''
    __PASSWORD: str = ''
    __HOST: str = ''
    __DB_NAME: str = ''

    def __init__(self, type_connect: str = 'async'):
        settings = configparser.ConfigParser()
        settings.read('data.ini')
        
        db = settings['DATABASE']
        self.__USERNAME = db['USERNAME']
        self.__PASSWORD = db['PASSWORD']
        self.__HOST = db['HOST']
        self.__DB_NAME = db['DB_NAME']
        
        self.token = settings['TOKEN']['token']
        self.admin = int(settings['ADMIN']['admin'])
        
        connectors = {
            'async': create_async_engine(self.async_connect_url, 
                                         pool_size=5,          # максимальное количество соединений в пуле
                                         max_overflow=10
                                         ),
            'sync': create_engine(self.sync,
                                  pool_size=5,          # максимальное количество соединений в пуле
                                  max_overflow=10)
        }

        self.engine: AsyncEngine = connectors[type_connect]
        
    @property
    def async_connect_url(self):
        return f'mysql+aiomysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'
    
    @property
    def sync(self):
        return f'mysql+pymysql://{self.__USERNAME}:{self.__PASSWORD}@{self.__HOST}/{self.__DB_NAME}'


cfg = Configurator()