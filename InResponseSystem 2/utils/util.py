import os
import time
import mysql
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling
import streamlit as st


connection = None 
@st.cache_resource 
def create_db_connection(host_name='sql12.freemysqlhosting.net', user_name='sql12611655',
                          user_password='ItD8sPSJru', db_name='sql12611655'
                          ):    # connection = None 
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name

        )
        cursor = connection.cursor()
        # connection = mysql.connector.connect(**st.secrets["mysql"])
        # st.info("Database connection successful")
    except Error as err:
        os.system('service mysql start')
        st.info(f"Error: '{err}'")
        cursor = connection.cursor()

    else:
        os.system('somthing else')
    return connection

def execute_query(connection, query):
    cursor = None
    try:
        
        cursor = connection.cursor()
    except Exception:
        os.system('service mysql start')
        time.sleep(2)
        cursor = connection.cursor()

    try:
        cursor.execute(query)
        connection.commit()
        st.info("Query successful")
    except Error as err:
        st.info(f"Error: '{err}'")


def read_query(connection, query):
    cursor = None
    try:
        cursor = connection.cursor()
        result = None
    except Exception:
        st.info("Starting MySQL Server....")
        cursor = connection.cursor()
    try:
        
        cursor.execute(query)
        result = cursor.fetchall()
        # st.info("Info Pull successful")
        return result
    except Error as err:
        st.info(f"Error: '{err}'")

def __Create_Tabels(connection):
    create_table = """
    CREATE TABLE users (
    id INT AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
    );
    """
    execute_query(connection,create_table)

def call_users():
    connection = create_db_connection()
    usernameQ = """ SELECT `username` FROM `users`"""
    nameQ =  """ SELECT `name` FROM `users` """
    passQ = """ SELECT `password` FROM `users` """

    r1 = read_query(connection,usernameQ)
    r2 = read_query(connection,nameQ)
    r3 = read_query(connection,passQ)
    usernames = []
    names = []
    passwords = []

    for row in r1:
        row  = ''.join(letter for letter in row if letter.isalnum())
        usernames.append(row)
        
    for row in r2:
        # row  = ''.join(letter for letter in row if letter.isalnum())
        names.append(row)
    for row in r3:
        row  = ''.join(letter for letter in row if letter.isalnum())
        passwords.append(row)

    return usernames,names,passwords

# connection = create_db_connection()
# __Create_Tabels(connection)



q0 = """
"INSERT INTO users (username, password, name, email)
 VALUES (%s, %s, %s, %s)"
"""
q11 = """ SELECT * FROM users """
q2 = """ 
INSERT INTO users ( username, password, name , email) VALUES ('noof', SHA2('noof', 256),'Noof', 'noof@gmail.com');
"""
q3 = """ 
INSERT INTO users ( username, password, name , email) VALUES ('admin', SHA2('admin', 256),'Noof', 'noof@gmail.com');
"""
delQ= """ DELETE FROM users WHERE id=8;"""

# connect_timeout: Number of seconds the mysqld server waits for a connect packet before responding with 'Bad handshake'
# interactive_timeout Number of seconds the server waits for activity on an interactive connection before closing it
# wait_timeout Number of seconds the server waits for activity on a connection before closing it

globalQ1= """ SET GLOBAL connect_timeout=28800 """
globalQ2= """ SET GLOBAL interactive_timeout=28800 """
globalQ3= """ SET GLOBAL wait_timeout=28800 """


Qq= """ SHOW GRANTS FOR 'sql12609927'@'ec2-52-8-112-233.us-west-1.compute.amazonaws.com';"""
q1="""UPDATE mysql.user SET max_user_connections = 0
WHERE user='sql12611655' AND host='sql12.freemysqlhosting.net';
FLUSH PRIVILEGES;"""
# execute_query(connection,q1)


# r = read_query(connection,q1)

# for row in r:
#     print(row)

# connection.query('SET GLOBAL connect_timeout=28800')
# connection.query('SET GLOBAL interactive_timeout=28800')
# connection.query('SET GLOBAL wait_timeout=28800')


