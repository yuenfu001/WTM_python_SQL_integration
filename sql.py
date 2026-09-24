from mysql import connector
from decouple import config

connection = connector.connect(
    host=config("host"),
    database=config("database"),
    port=config("port",cast=int),
    user=config("user"),
    password=config("password"),
)
if connection.is_connected():
    print("Congratulations! you are have successfully connected to mySQL server,wtm_backend_dev database")
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES;")
    # print(type(cursor.fetchall()))
    print("==== AVAILABLE DATABASES ====")
    for db in cursor.fetchall():
        print(f"- {db[0]}")
    cursor.execute("USE wtm_backend_dev;")
    # cursor.execute("CREATE TABLE franco(username VARCHAR(40), password VARCHAR(20),city VARCHAR(40));")
    # cursor.execute("SHOW COLUMNS FROM franco;")
    query = """
        INSERT INTO franco(username,password,city) VALUES (%s,%s,%s);
"""
    data=("franco001","idnotknow01","Kampala")
    cursor.execute(query,data)
    connection.commit()
    for table in cursor.fetchall():
        # print(f"{table[0]} | {table[1]} | {table[2]} | {table[3]}")
        print(f"{table}")
    # print(type(cursor.fetchall(dictionary=True)))
else:
    print(f"You did a wrong configuration, try again")