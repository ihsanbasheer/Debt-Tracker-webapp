import sqlite3
import numpy as np
from modules import bcrypt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_database_connection():
    return sqlite3.connect("debttracker.db")


CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
"""

CREATE_DEBT_TABLE = """
CREATE TABLE IF NOT EXISTS debttable (
    
    person TEXT,
    amount INTEGER,
    type TEXT NOT NULL,
    date DATE NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
"""



def checktable():
    with get_database_connection() as connect:
        d = connect.cursor()
        tables = ["debttable","users"]
        # SELECT {tables[0]} FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tables[0]}';"
        query1 = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tables[1]}';"
        d.execute(query)
        result = d.fetchone()
        d.execute(query1)
        result1 = d.fetchone()
        
        if not result:
            d.execute(CREATE_DEBT_TABLE)
            
        if not result1:
            d.execute(CREATE_USERS_TABLE)    
            
def get_plot(i): 
    with get_database_connection() as connect:
    
        d=connect.cursor()
        query =f'SELECT * FROM debttable WHERE type = "debt" AND user_id = ?'
        d.execute(query,(str(i),) )
        x = d.fetchall()
        query1 =f'SELECT * FROM debttable WHERE type = "owed" AND user_id = ?'
        d.execute(query1,(str(i),) )
        o = d.fetchall()
        print(o)
        names = [n[0] for n in x]
        amount = [n[1] for n in x]
        onames = [n[0] for n in o]
        oamount = [n[1] for n in o]


        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)  # 2 rows, 1 column, plot 1 (top plot)
        plt.bar(names, amount, color='skyblue')
        plt.xlabel('Amount',color="white")
        plt.ylabel('Names',color="white")
        plt.title('Debt Distribution',color="white")
        plt.gca().tick_params(axis='x', colors='white')  
        plt.gca().tick_params(axis='y', colors='white')

       
        plt.subplot(1, 2, 2)  # 2 rows, 1 column, plot 1 (top plot)
        plt.bar(onames, oamount, color='skyblue')
        plt.xlabel('Amount',color="white")
        plt.ylabel('Names',color="white")
        plt.title('Owed Distribution',color="white")
        plt.gca().tick_params(axis='x', colors='white')  
        plt.gca().tick_params(axis='y', colors='white')
        plt.tight_layout()
         
    return plt 

def register_user(username,password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    with get_database_connection() as connect:
        d=connect.cursor()
        query = f'INSERT INTO users(username,password) VALUES (?, ?)'
        d.execute(query,(username,hashed_password) )
        connect.commit()
        

def check_user_unique(username):
    with get_database_connection() as connect:
        d=connect.cursor()
        query = f'SELECT username FROM users WHERE username == ?'
        d.execute(query,(username,) )
        x = d.fetchall()
        if len(x) == 0:
            # print("no user")
            return True
        else:
            # print("user exists")
            return False
        
def get_password(username):
    with get_database_connection() as connect:
        d=connect.cursor()
        query = f'SELECT password FROM users WHERE username == ?'
        d.execute(query,(str(username),) )
        x = d.fetchone()
        if x:
            return x[0]
def get_id(username):
    with get_database_connection() as connect:
        d=connect.cursor()
        query = f'SELECT id FROM users WHERE username == ?'
        d.execute(query,(str(username),) )
        x = d.fetchone()
        if x:
            return x[0]              