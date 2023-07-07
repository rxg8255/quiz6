from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.config['UPLOAD_PATH'] = "./uploads"
app.secret_key = 'your secret key'

server = 'cse6332-db-server.database.windows.net'
username = 'cse6332-user'
password = 'Test@123'
database = 'quiz0'
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        session['user'] = user
        if user == 'admin':
            return redirect(url_for('store'))
        else:
            return redirect(url_for('userpage'))
    return render_template('login.html') 

@app.route('/store', methods=['GET', 'POST'])
def store():
    msg = ''
    sql = ('''
        SELECT * FROM items
        ''')
    cursor.execute(sql)
    items = cursor.fetchall()
    if request.method == 'POST':
        its = request.form['i']
        add_items = its.split(',')
        print(add_items)
        for a in add_items:
            if a.split()[1] in str(items):
                sql = '''SELECT qty FROM items where name=?'''
                cursor.execute(sql, (a.split()[1].strip()))
                qty = cursor.fetchone()
                print(qty)
                val = int(qty[0]) + int(a.split()[0].strip())
                sql = '''UPDATE items SET qty=? WHERE name=?''' 
                cursor.execute(sql, (val,a.split()[1].strip()))
            else:
                sql = '''INSERT INTO items (name, qty) VALUES (?,?)'''
                cursor.execute(sql, (a.split()[1].strip(),a.split()[0].strip()))
            cursor.commit()
            msg = 'Added successfully'
        return render_template('store.html', msg=msg)
    return render_template('store.html', items=items)

@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    msg = ''
    sql = '''SELECT items from orders where name=?'''
    cursor.execute(sql, (session['user']))
    items = cursor.fetchall()
    if request.method == 'POST':
        its = request.form['i']
        add_items = its.split(',')
        for a in add_items:
            sql = '''INSERT INTO orders (name, items) VALUES (?,?)'''
            cursor.execute(sql, (session['user'],a))
            sql = '''SELECT qty FROM items where name=?'''
            cursor.execute(sql, (a.split()[1].strip()))
            qty = cursor.fetchone()
            if int(a.split()[0].strip()) >= int(qty[0]):
                msg = 'Inventory unavailable - ' + a.split()[1].strip()
                return render_template('userpage.html', msg=msg)
            else:
                val = int(a.split()[0].strip()) - int(qty[0])
            sql = '''UPDATE items SET qty=? WHERE name=?''' 
            cursor.execute(sql, (val,a.split()[1].strip()))
            cursor.commit()
        msg = 'Order placed successfully'
        sql = '''SELECT items from orders where name=?'''
        cursor.execute(sql, (session['user']))
        items = cursor.fetchall()
        return render_template('userpage.html', items=items)
    return render_template('userpage.html', items=items)

