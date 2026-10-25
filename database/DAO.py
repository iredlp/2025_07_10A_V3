from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategories():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.category_name as category_name
                        from categories c """
        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(nomeC):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct p.*
                    from products p , categories c 
                    where c.category_name =%s
                    and p.category_id  =c.category_id   """

        cursor.execute(query, (nomeC,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProdottiPerPeriodo(nameP, anno1, anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select  distinct o.order_id as product_id
                from  order_items oi , orders o ,categories c 
                where oi.product_id = %s
                and o.order_id =oi.order_id 
                and o.order_date between %s and %s; """

        cursor.execute(query, (nameP, anno1, anno2))

        for row in cursor:
            results.append(row["product_id"])

        cursor.close()
        conn.close()
        return results