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
        d.execute('SELECT * FROM owedtable' )
        o = d.fetchall()
        names = [n[0] for n in x]
        amount = [n[1] for n in x]
        onames = [n[0] for n in o]
        oamount = [n[1] for n in o]

        plt.figure(figsize=(9, 5))
        plt.subplot(1, 2, 1)  # 2 rows, 1 column, plot 1 (top plot)
        plt.barh(names, amount, color='skyblue')
        plt.xlabel('Amount',color="white")
        plt.ylabel('Names',color="white")
        plt.title('Debt Distribution',color="white")
        plt.gca().tick_params(axis='x', colors='white')  
        plt.gca().tick_params(axis='y', colors='white')

       
        plt.subplot(1, 2, 2)  # 2 rows, 1 column, plot 1 (top plot)
        plt.barh(onames, oamount, color='skyblue')
        plt.xlabel('Amount',color="white")
        plt.ylabel('Names',color="white")
        plt.title('Owed Distribution',color="white")
        plt.gca().tick_params(axis='x', colors='white')  
        plt.gca().tick_params(axis='y', colors='white')
        plt.tight_layout()

         
    return plt 


