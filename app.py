from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import os
from werkzeug.utils import secure_filename
import blob_access

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
@app.route('/people', methods=['GET', 'POST'])
def users():
    cursor.execute('SELECT * FROM q0c')
    people = cursor.fetchall()
    if request.method == 'POST':
        search = request.form['search']
        rangefrom = request.form['rangefrom']
        rangeto = request.form['rangeto']
        print(rangefrom)
        print(rangeto)
        temp_people = []
        for p in people:
            if search in p[2]:
                temp_people.append(p)
        return render_template('people.html', people=temp_people)
    else:
        return render_template('people.html', people=people)

@app.route('/addrecord', methods=['GET', 'POST'])
def addrecord():
    msg=''
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        room = request.form['room']
        image = request.files['image']
        keywords = request.form['keywords']
        filename = filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        upload_status = blob_access.upload_blob(filename)
        print(upload_status)
        if upload_status[0] == 'Success':
            temp_filename = upload_status[1]
            picture_url = 'https://cse6332sa.blob.core.windows.net/images/' + temp_filename
        else:
            msg = 'Failed to upload file!!'
            return render_template('addrecord.html', msg=msg)
        sql = ('''
        SELECT * FROM q0c WHERE teln=?
        ''')
        cursor.execute(sql, (phone))
        account = cursor.fetchone()
        if account:
            msg = 'Record already exists'
        elif not name or not phone or not room or not keywords:
            msg = 'Please fill all details'
        else:
            cursor.execute('''INSERT INTO q0c (name,teln,room,picture_url,descript) 
                            VALUES (?, ?, ?, ?, ?)'''
                         , (name, phone, room, picture_url, keywords))
            cursor.commit()
            msg = 'You have successfully added !'
            return render_template('addrecord.html', msg=msg)
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('addrecord.html', msg=msg)

@app.route('/updaterecord/<id>', methods=['GET', 'POST'])
def updaterecord(id):
    msg=''
    cursor.execute('''SELECT * FROM q0c where id=?''', (id))
    record = cursor.fetchone()
    return render_template('updaterecord.html', person=record)

@app.route('/rupdate', methods=['GET', 'POST'])
def rupdate():
    msg='Failed to update'
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        phone = request.form['phone']
        room = request.form['room']
        keywords = request.form['keywords']
        if request.files['image']:
            print('IN')
            image = request.files['image']
            filename = filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            upload_status = blob_access.upload_blob(filename)
            print(upload_status)
            if upload_status[0] == 'Success':
                temp_filename = upload_status[1]
                picture_url = 'https://cse6332sa.blob.core.windows.net/images/' + temp_filename
                cursor.execute('''UPDATE q0c SET picture_url=? WHERE id=?''',(picture_url, id))

        cursor.execute("UPDATE q0c SET name='{}', teln='{}', descript='{}', room='{}' "
                     "where id={}".format(name, phone, keywords, room, id))
        cursor.commit()
        msg = 'Record successfully updated !'
        return redirect('/')
    return render_template('updaterecord.html', msg=msg)

@app.route('/deleterecord/<id>', methods=['GET', 'POST'])
def deleterecord(id):
    msg=''
    cursor.execute("DELETE FROM q0c where id={}".format(id))
    cursor.commit()
    msg = 'Record successfully deleted !'
    return redirect('/')