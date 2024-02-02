import psycopg2
import csv

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="Zz123456"
)

# Create a cursor object
cur = conn.cursor()

# Define a function to import CSV data into a PostgreSQL table
def import_csv_to_postgres(filename, table_name):
    # Truncate the main table and all dependent tables (CASCADE)
    truncate_query = f'TRUNCATE TABLE "{table_name}" CASCADE;'
    cur.execute(truncate_query)
    conn.commit()

    # Use COPY command to import data into the table
    copy_query = f'COPY "{table_name}" FROM stdin WITH CSV HEADER DELIMITER as \',\';'
    with open(filename, 'r', newline='', encoding='utf-8') as datafile:
        cur.copy_expert(sql=copy_query, file=datafile)

    conn.commit()




# Import each CSV file into the corresponding table
import_csv_to_postgres('customers.csv', 'customer')
import_csv_to_postgres('items.csv', 'item')
import_csv_to_postgres('sellers.csv', 'seller')
import_csv_to_postgres('goods.csv', 'good')
import_csv_to_postgres('orders.csv', 'order')

# Close the cursor and connection
cur.close()
conn.close()
