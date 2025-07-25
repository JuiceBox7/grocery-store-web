from sql_connection import get_sql_connection


def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM products"
    cursor.execute(query)
    response = []

    for product_id, name, uom_id, price_per_unit in cursor:
        response.append(
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
            }
        )

def insert_product(connection, product):
    cursor = connection.cursor()
    query = "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)"
    data = (product["product_name"], product["uom_id"], product["price_per_unit"])
    cursor.execute(query, data)

    connection.commit()
    return cursor.lastrowid


def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = "DELETE FROM products WHERE product_id= %s"
    cursor.execute(query, (product_id,))
    connection.commit()


if __name__ == "__main__":
    connection = get_sql_connection()
