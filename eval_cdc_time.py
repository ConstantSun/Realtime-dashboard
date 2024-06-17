import psycopg2
import time
import random
import string

# Source database connection details
src_db_user = "adminuser"
src_db_password = "admin123"
src_db_host = "dmslabinstance.cafqx7kxfmqe.us-east-1.rds.amazonaws.com" 
src_db_name = "tps_src"
src_db_schema = "tps_src" 

# Destination database connection details
dst_db_user = "adminuser"
dst_db_password = "admin123"
dst_db_host =  "rds-destination-poc.cafqx7kxfmqe.us-east-1.rds.amazonaws.com"
dst_db_name =  "postgres"
dst_db_schema = "tps_dst4"

# Function to generate a random client name
def generate_client_name():
    letters = string.ascii_lowercase
    client_name = ''.join(random.choice(letters) for _ in range(10))
    return client_name

# Function to create a new client in the source database
def create_client(conn, client_id, client_name):
    cur = conn.cursor()
    query = f"INSERT INTO {src_db_schema}.client (client_id, full_name) VALUES ('{client_id}', '{client_name}');"
    cur.execute(query)
    conn.commit()
    cur.close()

# Function to retrieve the newly created client from the destination database
def get_client(conn, client_name):
    cur = conn.cursor()
    query = f"SELECT client_id, full_name FROM {dst_db_schema}.client WHERE full_name = '{client_name}';"
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    return result

# Connect to the source database
src_conn = psycopg2.connect(
    user=src_db_user,
    password=src_db_password,
    host=src_db_host,
    database=src_db_name
)

# Connect to the destination database
dst_conn = psycopg2.connect(
    user=dst_db_user,
    password=dst_db_password,
    host=dst_db_host,
    database=dst_db_name
)

# Generate a random client name
# client_name = generate_client_name()
client_id = 'C234567'
client_name = "fuligo"

# Create a new client in the source database
create_client(src_conn, client_id, client_name)

# Wait for the change to be reflected in the destination database
start_time = time.perf_counter()
while True:
    result = get_client(dst_conn, client_name)
    if result:
        break
    time.sleep(0.001)  # Sleep for 1 millisecond

end_time = time.perf_counter()
elapsed_time_ms = (end_time - start_time) * 1000

# Print the newly created client and the time taken for the change to be reflected
print(f"New client created: {result}")
print(f"Time taken for the change to be reflected: {elapsed_time_ms:.2f} milliseconds")

# Close the database connections
src_conn.close()
dst_conn.close()