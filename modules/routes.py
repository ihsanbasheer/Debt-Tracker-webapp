import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from modules import app
from modules.database import checktable,get_plot,register_user,check_user_unique,check_password

import sqlite3

checktable()

load_dotenv()


@app.route('/', methods=["GET"])
def redir():
    if 'username' in session:
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        loginuser = request.form["LOGINU"] 
        loginpass = request.form["LOGINP"]

        if check_password(loginuser) == loginpass:
            session['username'] = loginuser
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password", "error")
            
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "POST":
        registeruser = request.form["REGISTERU"] 
        registerpass = request.form["REGISTERP"]
        registerconfirmpass = request.form["CONFIRMREGISTERP"]

        if check_user_unique(registeruser) and registerpass == registerconfirmpass:
            register_user(registeruser,registerpass)
            flash("Registered user successfully", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid username or password", "error")
            
    return render_template('register.html')

@app.route('/home', methods=["GET", "POST"])
def welcome():
    if 'username' in session:
        connect = sqlite3.connect("debtowed_info.db")
        d=connect.cursor()
        d.execute('SELECT COALESCE(SUM(amount), 0) FROM debttable')
        sumdebt = d.fetchone()[0]
        d.execute('SELECT COALESCE(SUM(amount), 0) FROM owedtable')
        sumowed = d.fetchone()[0]
        
        plot = get_plot() 
  
        # Save the figure in the static directory 
        plot.savefig(os.path.join( 'modules','static', 'images', 'plot.png'))
        print("plot saved")
                     
        return render_template("home.html",x=sumdebt,y=sumowed)
    else:
        return redirect(url_for('login'))
    
@app.route('/add_or_remove', methods=['POST', 'GET'])
def modify():
    return render_template("add_or_remove.html",formvisible = False )

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/viewdebt', methods =["POST","GET"])
def debttable():
    connect = sqlite3.connect("debtowed_info.db")
    d=connect.cursor()
    d.execute('SELECT * FROM debttable' )
    x = d.fetchall()
    return render_template("viewdebt.html",x=x)

@app.route('/viewowed', methods =["POST","GET"])
def owedtable():
    connect = sqlite3.connect("debtowed_info.db")
    d=connect.cursor()
    d.execute('SELECT * FROM owedtable' )
    y = d.fetchall()
    return render_template("viewowed.html",y=y)


@app.route('/add', methods=['POST', 'GET'])
def addperson():
    connect = sqlite3.connect("debtowed_info.db")
    d=connect.cursor()
    if request.method == 'POST':
        table = session["table"]    
        inputperson = request.form["personname"] 
        inputamount = request.form["amount"] 
        query = f'INSERT INTO {table} VALUES (?, ?)'
        d.execute(query,(inputperson,inputamount) )
        connect.commit()

        connect.close()

        return redirect(url_for(table))

@app.route('/delete', methods=["POST", "GET"])
def deleter():
    connect = sqlite3.connect("debtowed_info.db")
    d=connect.cursor()
    debt_or_owed =  request.form.get("optiondebt")
    table = session["table"]
    remove= request.form["remove"]
    query = f'DELETE FROM {table} WHERE person==?'
    d.execute(query,(remove,))
    connect.commit()
    return redirect(url_for(table))

@app.route('/update', methods=["POST", "GET"])
def updater():
    connect = sqlite3.connect("debtowed_info.db")
    d=connect.cursor()
    person_update= request.form["update_personname"]
    amount_update = request.form["update_amount"]
    debt_or_owed =  request.form.get("optiondebt")
    table = session["table"]
    query = f"UPDATE {table} SET amount =? WHERE person ==?"    
    d.execute(query,(amount_update,person_update) )
    connect.commit()
    return redirect(url_for(table))


@app.route('/debt_or_owed', methods =["POST","GET"])
def formactivity():
    debt_or_owed =  request.form.get("optiondebt")
    if debt_or_owed:
        session["formvisible"] = True
        session["table"] = debt_or_owed
              
    return render_template("add_or_remove.html",z=request.form.get("optiondebt"),formvisible=session["formvisible"])