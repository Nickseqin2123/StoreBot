import pymysql
import pymysql.cursors


class RequestsFirst:

    HOST = "127.0.0.1"
    USER = "root"
    PASSWORD = "NekitVip123_ZXCPUDGE228"
    DATABASE = "users"

    def get_products(self, product_name=None):
        try:
            connect = pymysql.connect(
                host=self.HOST,
                database=self.DATABASE,
                password=self.PASSWORD,
                port=3306,
                user=self.USER,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    if product_name:
                        cursa.execute(f"""SELECT * FROM store.products
                                      WHERE product = '{product_name}'""")
                        return cursa.fetchall()
                    cursa.execute("SELECT * FROM store.products")
                    return cursa.fetchall()
            finally:
                connect.close()
                    
        except Exception as er:
            print(er)

    def get_card(self):
        try:
            connect = pymysql.connect(
                host=self.HOST,
                database=self.DATABASE,
                password=self.PASSWORD,
                port=3306,
                user=self.USER,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    cursa.execute("SELECT * FROM store.card")
                    return cursa.fetchall()
            finally:
                connect.close()
                    
        except Exception as er:
            print(er)

    def set_product(self, product_name: str, count: int, price: int | float):
        try:
            connect = pymysql.connect(
                host=self.HOST,
                database=self.DATABASE,
                password=self.PASSWORD,
                port=3306,
                user=self.USER,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    if self.get_products(product_name):
                        req = f"""UPDATE `store`.`products`
                        SET count = `count` + '{count}',
                        price = '{price}'
                        WHERE product = '{product_name}'"""
                    else:
                        req = f"""INSERT INTO `store`.`products` (`product`, `count`, `price`)
                        VALUES ('{product_name}', '{count}', '{price}')"""
                    cursa.execute(req)
                    connect.commit()
                    
            finally:
                connect.close()
                    
        except Exception as er:
            print(er)

    def sub_product(self, product_name: str, count: int, price: int | float):
        try:
            connect = pymysql.connect(
                host=self.HOST,
                database=self.DATABASE,
                password=self.PASSWORD,
                port=3306,
                user=self.USER,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    req = f"""UPDATE `store`.`products`
                    SET count = `count` - '{count}',
                    price = '{price}'
                    WHERE product = '{product_name}'"""
                    cursa.execute(req)
                    connect.commit()
                    
            finally:
                connect.close()
                    
        except Exception as er:
            print(er)

    def delete_product(self, product_name):
        try:
            connect = pymysql.connect(
                host=self.HOST,
                port=3306,
                database=self.DATABASE,
                user=self.USER,
                password=self.PASSWORD,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("OK")
            try:
                with connect.cursor() as cursa:
                    req = f"""DELETE FROM `store`.`products` WHERE `product` = '{product_name}'"""
                    cursa.execute(req)
                    connect.commit()

            finally:
                connect.close()

        except Exception as er:
            print(er)