import pymysql
import pymysql.cursors

from SqlRequest.RequestsFirst import RequestsFirst



class RequestsSecond(RequestsFirst):
    
    
    def get_user_card(self, user_id):
        try:
            connect = pymysql.connect(
                password=self.PASSWORD,
                database=self.DATABASE,
                port=3306,
                user=self.USER,
                host=self.HOST,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    cursa.execute(f"SELECT * FROM `store`.`card` WHERE user_id = {user_id}")
                    return cursa.fetchall()
            finally:
                connect.close()
        
        except Exception as er:
            print(er)
    
    
    def get_products(self):
        return super().get_products()
    
    
    def add_user_card(self, user_id: int, product_name: str, count: int, price: int|float):
        try:
            connect = pymysql.connect(
                password=self.PASSWORD,
                database=self.DATABASE,
                port=3306,
                user=self.USER,
                host=self.HOST,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    if product_name in [i['product'] for i in self.get_user_card(user_id)]:
                        req = f"""UPDATE `store`.`card`
                        SET count = `count` + '{count}'
                        WHERE (`user_id` = '{user_id}' AND `product` = '{product_name}')"""
                    else:
                        req = f"""INSERT INTO `store`.`card`
                        (`product`, `user_id`, `count`, `price`)
                        VALUES ('{product_name}', '{user_id}', '{count}', '{price}')"""
                    cursa.execute(req)
                    connect.commit()
                    
            finally:
                connect.close()
                self.sub_product(product_name, count, price)
        
        except Exception as er:
            print(er)
    
    
    def sub_user_card(self, user_id: int, product_name: str, count: int):
        try:
            connect = pymysql.connect(
                password=self.PASSWORD,
                database=self.DATABASE,
                port=3306,
                user=self.USER,
                host=self.HOST,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    req = f"""UPDATE `store`.`card`
                    SET count = `count` - '{count}'
                    WHERE (`user_id` = '{user_id}' AND `product` = '{product_name}')"""
                    cursa.execute(req)
                    connect.commit()
                    
            finally:
                connect.close()
        
        except Exception as er:
            print(er)
    
    
    def set_user(self, user_id):
        try:
            connect = pymysql.connect(
                password=self.PASSWORD,
                database=self.DATABASE,
                port=3306,
                user=self.USER,
                host=self.HOST,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    cursa.execute(f"SELECT * FROM store.user WHERE user_id = {user_id}")
                    fetch = cursa.fetchall()
                    if bool(fetch) is False:
                        req = f"""INSERT INTO `store`.`user` (`user_id`) VALUES ('{user_id}')"""
                        cursa.execute(req)
                        connect.commit()
                    
            finally:
                connect.close()
        
        except Exception as er:
            print(er)
            

database = RequestsSecond()