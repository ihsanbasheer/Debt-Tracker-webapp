import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from modules import app
from modules.database import checktable,get_plot,register_user,check_user_unique,check_password,get_id

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
            session['user_id'] = get_id(loginuser)
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
        user_id = session['user_id']
        connect = sqlite3.connect("debttracker.db")
        d=connect.cursor()
        d.execute('SELECT COALESCE(SUM(amount), 0) FROM debttable WHERE type = "debt" AND user_id = ?',(user_id,))
        sumdebt = d.fetchone()[0]
        d.execute('SELECT COALESCE(SUM(amount), 0) FROM debttable WHERE type = "owed" AND user_id = ?',(user_id,))
        sumowed = d.fetchone()[0]
        
        plot = get_plot(user_id) 
  
        # Save the figure in the static directory 
        plot.savefig(os.path.join( 'modules','static', 'images', 'plot.png'),transparent=True)
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
    session.pop('user_id',None)
    return redirect(url_for('login'))


@app.route('/viewdebt', methods =["POST","GET"])
def debt():
    user_id = session['user_id']
    connect = sqlite3.connect("debttracker.db")
    d=connect.cursor()
    d.execute('SELECT * FROM debttable WHERE type = "debt" AND user_id == ?',(user_id,) )
    x = d.fetchall()
    return render_template("viewdebt.html",x=x)

@app.route('/viewowed', methods =["POST","GET"])
def owed():
    user_id = session['user_id']
    connect = sqlite3.connect("debttracker.db")
    d=connect.cursor()
    d.execute('SELECT * FROM debttable WHERE type = "owed" AND user_id == ?',(user_id,))
    y = d.fetchall()
    return render_template("viewowed.html",y=y)


@app.route('/add', methods=['POST', 'GET'])
def addperson():
    
    connect = sqlite3.connect("debttracker.db")
    d=connect.cursor()
    if request.method == 'POST':
        table = session["table"]
        user_id = session['user_id']    
        inputperson = request.form["personname"] 
        inputamount = request.form["amount"]
        debt_or_owed =  session["table"]
        query = f'INSERT INTO debttable(person,amount,type,user_id) VALUES(?,?,?,?)'
        print("Query:", inputperson, inputamount, debt_or_owed, user_id)  # Print the query string
        d.execute(query, (inputperson, inputamount, debt_or_owed, user_id))
        connect.commit()

        connect.close()

        return redirect(url_for(table))

@app.route('/delete', methods=["POST", "GET"])
def deleter():
    user_id = session['user_id']
    connect = sqlite3.connect("debttracker.db")
    d=connect.cursor()
    debt_or_owed =  session["table"]
    table = session["table"]
    remove= request.form["remove"]
    query = f'DELETE FROM debttable WHERE person==? AND type ==? AND user_id == ?'
    d.execute(query,(remove,debt_or_owed,user_id))
    connect.commit()
    return redirect(url_for(table))

@app.route('/update', methods=["POST", "GET"])
def updater():
    user_id = session['user_id']
    connect = sqlite3.connect("debttracker.db")
    d=connect.cursor()
    person_update= request.form["update_personname"]
    amount_update = request.form["update_amount"]
    debt_or_owed =  session["table"]
    table = session["table"]
    query = f"UPDATE debttable SET amount =? WHERE person ==? AND type ==? AND user_id == ?"    
    d.execute(query,(amount_update,person_update,debt_or_owed,user_id) )
    connect.commit()
    return redirect(url_for(table))


@app.route('/debt_or_owed', methods =["POST","GET"])
def formactivity():
    debt_or_owed = request.form['optiondebt']
    if debt_or_owed:
        session["formvisible"] = True
        session["table"] = debt_or_owed
              
    return render_template("add_or_remove.html",z=debt_or_owed,formvisible=session["formvisible"])