import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_database_connection():
    return sqlite3.connect("debtowed_info.db")


CREATE_DEBT_TABLE = """
CREATE TABLE IF NOT EXISTS debttable (
    person TEXT,
    amount INTEGER
)
"""

CREATE_OWED_TABLE = """
CREATE TABLE IF NOT EXISTS owedtable (
    person TEXT,
    amount INTEGER
)
"""

def checktable():
    with get_database_connection() as connect:
        d = connect.cursor()
        tables = ["debttable","owedtable"]
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tables[0]}';"
        query1 = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tables[1]}';"
        d.execute(query)
        result = d.fetchone()
        d.execute(query1)
        result1 = d.fetchone()
        
        if not result:
            d.execute(CREATE_DEBT_TABLE)
            
        if not result1:
            d.execute(CREATE_OWED_TABLE)    
            
def get_plot(): 
    with get_database_connection() as connect:
    
        d=connect.cursor()
        d.execute('SELECT * FROM debttable' )
        x = d.fetchall()
        names = [n[0] for n in x]
        amount = [n[1] for n in x]
        
        plt.bar(names,amount, color='c' ) 
        plt.xlabel('Names') 
        plt.ylabel('Amount')
        plt.title('debt distribution')
         
    return plt 


