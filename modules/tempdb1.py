# import sqlite3

# def get_database_connection():
#     return sqlite3.connect("debtowed_info.db")

# def check_user_unique(username):
#     with get_database_connection() as connect:
#         d=connect.cursor()
#         query = f'SELECT username FROM users WHERE username == ?'
#         d.execute(query,(username,) )
#         x = d.fetchall()
#         if len(x) == 0:
#             print("no user")
#             return True
#         else:
#             print("user exists")
#             return False
        
# def register_user(username,password):
#     with get_database_connection() as connect:
#         d=connect.cursor()
#         query = f'INSERT INTO users VALUES (?, ?)'
#         d.execute(query,(username,password) )
#         connect.commit()

# with get_database_connection() as connect:
#     d=connect.cursor()
#     u ="ihsan"
#     d.execute('SELECT password FROM users WHERE username == "?"', (u,) )
#     x = d.fetchone()
#     print(x[0])                               