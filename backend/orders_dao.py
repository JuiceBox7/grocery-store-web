from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()
    order_query = ("INSERT INTO orders (customer_name, total, datetime) VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())
    cursor.execute(order_query, order_data)

    order_details_query = ("INSERT INTO order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)")
    order_details_data = []
    order_id = cursor.lastrowid

    for order_details_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_details_record['product_id']),
            float(order_details_record['quantity']),
            float(order_details_record['total_price'])
        ])
    cursor.executemany(order_details_query, order_details_data)
    connection.commit()

    return order_id

def get_order_details(connection, order_id):
    cursor = connection.cursor()
    query = "SELECT order_details.order_id, order_details.quantity, order_details.total_price, products.name, \
        products.price_per_unit FROM order_details LEFT JOIN products ON order_details.product_id = products.product_id \
        WHERE order_details.order_id = %s"
    cursor.execute(query, order_id)
    records = []

    for order_id, quantity, total_price, product_name, price_per_unit in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })
    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    response = []

    for order_id, customer_name, total, dt in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt
        })
    cursor.close()

    for record in response:
        record['order_details'] = get_order_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
