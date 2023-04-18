import mysql.connector as mysqlconn
from mysql.connector import pooling as pooling
import streamlit as st

from mysql.connector import Error
from mysql.connector import pooling


usernames = []
names = []
passwords = []
global fetchUsers 
global connection_object 
connection_object =None
fetchUsers = []

def create_conn():
    try:
        connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                                    pool_size=5,
                                                    pool_reset_session=True,
                                                    host='sql7.freemysqlhosting.net',
                                                    database='sql7613171',
                                                    user='sql7613171',
                                                    password='Z7PbeZZAbW',
                                                    port=3306)

        print("Printing connection pool properties ")
        print("Connection Pool Name - ", connection_pool.pool_name)
        print("Connection Pool Size - ", connection_pool.pool_size)
        # Get connection object from a pool
        connection_object = connection_pool.get_connection()
        # connection_object = connection_pool.shutdown()

        if connection_object.is_connected():
            db_Info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

            cursor = connection_object.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to - ", record)

            

            cursor.execute(""" SELECT `username` FROM `users`""")
            recordUsers = cursor.fetchall()
        
            cursor.execute(""" SELECT `name` FROM `users` """)
            recordNames = cursor.fetchall()
            
            cursor.execute(""" SELECT `password` FROM `users` """)
            recordPass = cursor.fetchall()  
            

            for row in recordUsers:
                row  = ''.join(letter for letter in row if letter.isalnum())
                usernames.append(row)
                
            for row in recordNames:
                # row  = ''.join(letter for letter in row if letter.isalnum())
                names.append(row)
            for row in recordPass:
                row  = ''.join(letter for letter in row if letter.isalnum())
                passwords.append(row)
            #for users profiles:                     
            # cursor.execute('SELECT id, username , name, email FROM users;')
            # fetchUsers = cursor.fetchall() 
            # for row in fetchUsers:
            #     fetchUsers.append(row)
        return  connection_object   

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            print("MySQL connection is closed")

def close_conn():
    connection_object = create_conn()
    # closing database connection.
    if connection_object.is_connected():
        create_conn.cursor.close()
        connection_object.close()
        print("MySQL connection is closed")

def call_users(c):
    cursor = c.cursor()
    cursor.execute(""" SELECT `username` FROM `users`""")
    recordUsers = cursor.fetchall()
    cursor.execute(""" SELECT `name` FROM `users` """)
    recordNames = cursor.fetchall()
    cursor.execute(""" SELECT `name` FROM `users` """)
    recordPass = cursor.fetchall()   

    usernames = []
    names = []
    passwords = []

    for row in recordUsers:
        row  = ''.join(letter for letter in row if letter.isalnum())
        usernames.append(row)
        
    for row in recordNames:
        # row  = ''.join(letter for letter in row if letter.isalnum())
        names.append(row)
    for row in recordPass:
        row  = ''.join(letter for letter in row if letter.isalnum())
        passwords.append(row)

    return usernames,names,passwords


