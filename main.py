# imports
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/h.d.s'
db = SQLAlchemy(app)


class Userlist(db.Model):
    '''
    sno, phone_no, user_name, PAid, password, date
    '''

    sno = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String(13), unique=True, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    PAid = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route('/sign_up/', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        '''Adding user to the database'''

        phone_no = request.form.get('phone_no')
        user_name = request.form.get('user_name')
        PAid = request.form.get('PAid')
        password = request.form.get('password')
        data = datetime.datetime.now()

        connectt = mysql.connector.connect(host="localhost", user="root", password="", database="h.d.s")
        cursor = connectt.cursor()

        cursor.execute("""SELECT * FROM `userlist` WHERE `phone_no` LIKE '{}' AND `user_name` like '{}' AND 
        `PAid` like '{}'"""
                       .format(phone_no, user_name, PAid))
        OOO = cursor.fetchall()

        cursor.execute("""SELECT * FROM `userlist` WHERE `phone_no` LIKE '{}'"""
                       .format(phone_no))
        no = cursor.fetchall()

        cursor.execute("""SELECT * FROM `userlist` WHERE `user_name` like '{}'"""
                       .format(user_name))
        usr_id = cursor.fetchall()

        cursor.execute("""SELECT * FROM `userlist` WHERE `PAid` like '{}'"""
                       .format(PAid))
        id = cursor.fetchall()

        if len(OOO) == 0 and len(no) == 0 and len(usr_id) == 0 and len(id) == 0:
            entry = Userlist(phone_no=phone_no, user_name=user_name, PAid=PAid, password=password, date=data)
            db.session.add(entry)
            db.session.commit()
            msg = "User added."

        elif len(OOO) != 0 and len(no) != 0 and len(usr_id) != 0 and len(id) != 0:
            msg = "This user already exist."

        elif len(no) != 0:
            msg = "This phone number is already registered."

        elif len(usr_id) != 0:
            msg = "This USER NAME is already registered. Please try with another USER NAME."

        elif len(id) != 0:
            msg = "This PAid already registered. Please try with different PAid."

        return msg


@app.route('/log_in/', methods=['POST'])
def log_in():
    id = request.form.get('PAid')
    password = request.form.get('password')

    connectt = mysql.connector.connect(host="localhost", user="root", password="", database="h.d.s")
    cursor = connectt.cursor()

    cursor.execute("""SELECT * FROM `userlist` WHERE `phone_no` LIKE '{}' AND `password` like '{}'"""
                   .format(id, password))
    access_phone_no = cursor.fetchall()

    cursor.execute("""SELECT * FROM `userlist` WHERE `user_name` LIKE '{}' AND `password` like '{}'"""
                   .format(id, password))
    access_user_id = cursor.fetchall()

    cursor.execute("""SELECT * FROM `userlist` WHERE `PAid` LIKE '{}' AND `password` like '{}'"""
                   .format(id, password))
    access_PAid = cursor.fetchall()

    if len(access_phone_no) == 1:
        msg = "permission granted"
        print(access_phone_no)

    elif len(access_user_id) == 1:
        msg = "permission granted"
        print(access_user_id)

    elif len(access_PAid) == 1:
        msg = "permission granted"
        print(access_PAid)
    else:
        msg = "permission denied"
    return msg


if __name__ == "__main__":
    app.run(debug=True)
