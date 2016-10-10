
from flask import Flask, render_template, request, redirect, session, flash
import re
import md5
from flask_bcrypt import Bcrypt



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])[a-zA-Z\d]+$')

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'i<3secrets'

from mysqlconnection import MySQLConnector
mysql = MySQLConnector (app, 'registration')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods =['POST'])
def create():
    if len(request.form["first_name"])< 2:
        flash("First Name cannot be empty and more than 2 characters")
        return redirect('/')

    elif len(request.form["last_name"])< 2:
        flash("Last Name cannot be empty and more than 2 characters")
        return redirect('/')

    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Enter a valid email")
        return redirect('/')

    elif not len(request.form["password"])> 8:
        flash("Password should be longer than 8 characters")
        return redirect('/')

    elif not len(request.form["confirm_password"])> 8 :
        flash("Password should be longer than 8 characters")
        return redirect('/')

    elif not str(request.form["password"])== str(request.form["confirm_password"]):
        flash("Password do not match")
        return redirect('/')

    else:
        query = 'INSERT INTO users(first_name,last_name,email, password, confirm_password) values(:first_name, :last_name, :email,:password, :confirm_password)'
        data = {
        'first_name': request.form["first_name"],
        'last_name' : request.form["last_name"],
        'email': request.form["email"],

        'password': bcrypt.generate_password_hash(request.form['password']),
        'confirm_password': md5.new(request.form['confirm_password']).hexdigest()
        }
        mysql.query_db(query, data)

        flash("Registration Successful")
        return redirect('https://kariprax.wordpress.com/')

@app.route('/login', methods =['POST'])
def login():

    query = "SELECT password FROM users WHERE email = '" +request.form["email"]+ "';"
    info = mysql.query_db(query)
    if bcrypt.check_password_hash(info[0]['password'], request.form['password']):
        flash("Login Successful")
        return redirect('/')
    else:
        flash("Invalid email/password")
        return redirect('/')





# @app.route('/friends/<id>/edit',methods =['get'] )
# def edit(id):
#     return render_template('edit.html', id = id)
#
#
# @app.route('/friends/<id>', methods =['POST'])
# def update(id):
#     print id
#     query= 'UPDATE users SET First_name= :First_name, last_name =:last_name,email = :email, created_at = now() WHERE id =' +id;
#     data = {
#     'First_name': request.form["first_name"],
#     'last_name' : request.form["last_name"],
#     'email': request.form["email"],
#     }
#     mysql.query_db(query, data)
#     return redirect('/')
#
# @app.route('/friends/<id>/delete', methods =['POST'])
# def delete(id):
#     # return render_templateeturn redirect('/')"edit.html", username=id)
#      query = 'DELETE from users WHERE id = ' +id   ;
#      mysql.query_db(query)
#      print query
#      return redirect('/')
#
#
# # @app.route('/email', methods = ['POST'])
# # def checkemail():
# #     print request.form['email']
# #     if not EREG.match(request.form['email']):
# #         flash('Email is not vaild!')
# #         return redirect('/')
# #     else:
# #         query = 'insert into user_emails(email, created_at, updated_at) values(:email, now(), now())'
# #         data = {
# #         'email': request.form["email"]
# #         }
# #         mysql.query_db(query, data)
# #
# #         return redirect('/show')
# #
# #
# # @app.route('/show')
# # def show():
# #     flash('The email address you entered is a VALID email address!')
# #     query = 'SELECT * FROM emails.user_emails;'
# #     users = mysql.query_db(query)
# #     return render_template('success.html', users=users)

app.run(debug=True)
