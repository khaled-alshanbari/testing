import os
import time

import mysql.connector
import streamlit
from mysql.connector import Error
import pandas as pd


def create_conn(host_name='sql7.freemysqlhosting.net', user_name='sql7613171', user_password='Z7PbeZZAbW', db_name='sql7613171'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

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
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = None
    try:
        cursor = connection.cursor()
        result = None
    except Exception:
        streamlit.info("Starting MySQL Server....")
        os.system('service mysql start')
        time.sleep(5)
        cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

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


