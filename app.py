from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_mail import Mail, Message
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests
import random

#from signup_form import SignupForm
from second import second
from api import api
#from session import session

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465 #maybe change
app.config['MAIL_USERNAME'] = 'VectorNpProject@gmail.com'
app.config['MAIL_PASSWORD'] = 'npflask22'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.register_blueprint(second, url_prefix="")

app.register_blueprint(api, url_prefix="/api")

#app.register_blueprint(session, url_prefix="")

app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours = 24)

db = SQLAlchemy(app)





def random_pwd():
    pwd = ''
    for x in range(0, 11):
        if x % 2 == 0:
            pwd += chr(random.randint(97, 122))
        else:
            pwd += str(random.randint(0, 9))
    return pwd


@app.route('/email_processing')
def email_processing():
    if 'email' in session:
        msg = Message('Vector password reset', sender = 'VectorNpProject@gmail.com', recipients= [session['email']])
        password = random_pwd()
        print(session['email'])
        user = users.query.filter_by(email = session['email']).first()
        user.password = password
        db.session.commit
        msg.body = f"Hello {session['firstname']} {session['lastname']}! Your new password is: {password}"
        mail.send(msg)
        flash('Your new password is in your emails', 'success')
        return redirect(url_for('change_profile'))
    else:
        flash('An error occured', 'error')
        redirect(url_for('change_profile'))

 



class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    status = db.Column(db.String(100), default = 'guest')


    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password




class flights(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    user_id = db.Column('user_id', db.Integer)
    carrier_id = db.Column('carrier_id', db.Integer)
    price = db.Column('price', db.Integer)
    symbol = db.Column('symbol', db.String(1))
    departure_airport = db.Column('departure_airport', db.String(100))
    destination_airport = db.Column('destination_airport', db.String(100))
    date = db.Column('date', db.String(50))
    time = db.Column('time', db.String(50))

    def __init__(self, user_id, carrier_id, price, symbol, departure_airport, destination_airport, date, time):
        self.user_id = user_id
        self.carrier_id = carrier_id
        self.price = price
        self.symbol = symbol
        self.departure_airport = departure_airport
        self.destination_airport = destination_airport
        self.date = date
        self.time = time





@app.route('/', methods = ['GET', 'POST'])
def index():
    if 'firstname' in session:
        return render_template('index.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('index.html')



@app.route('/hotel', methods = ['GET', 'POST'])
def hotel():
    if 'firstname' in session:
        return render_template('hotels.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('hotels.html', navbarname = 'You need to sign in to purchase')





@app.route('/change_profile')
def change_profile():
    if 'firstname' in session:
        user = users.query.filter_by(firstname = session['firstname'], lastname = session['lastname']).first()
        firstname = user.firstname
        lastname = user.lastname
        email = user.email
        password = user.password
        if session['status'] == 'guest':
            return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email, navbarname = f"Hello {session['firstname']}")
        if session['status'] == 'admin':
            return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email, navbarname = f"Hello {session['firstname']}", users = users.query.filter_by(status = 'guest').all())
                #return render_template('show_all.html', users = users.query.all())
    else:
        return redirect(url_for('signin'))



        carrier_id = request.args.get('carrier_id')
        flight = flights.query.filter_by(carrier_id = carrier_id).first()
        db.session.delete(flight)
        db.session.commit()
        flash('Flight was deleted successfully.', 'success')
        return redirect(url_for('cart'))


@app.route('/delete_user', methods = ['GET'])
def delete_user():
    if request.method == 'GET':
        if not request.args.get('user_id'):
            flash('A problem has occured.', 'error')
            return redirect(url_for('change_profile'))
        else:
            user_id = request.args.get('user_id')
            user = users.query.filter_by(_id = user_id).first()
            db.session.delete(user)
            db.session.commit()
            flash('User deleted', 'success')
            return redirect(url_for('change_profile'))




@app.route('/change_profile_processing', methods = ['POST'])
def change_profile_processing():
    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email']:
            user = users.query.filter_by(firstname = session['firstname'], lastname = session['firstname']).first()
            session.pop('_flashes', None)
            flash('All fields are required.', 'error')
            return render_template('change_profile.html')
        else:
            old_firstname = session['firstname']
            old_lastname = session['lastname']
            user = users.query.filter_by(firstname = old_firstname, lastname = old_lastname).first()
            user.email = request.form['email']
            user.firstname = request.form['firstname']
            user.lastname = request.form['lastname']
            db.session.commit()
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            firstname = user.firstname
            lastname = user.lastname
            email = user.email
            flash('Changes done successfully', 'success')
            return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email)


@app.route('/trains', methods = ["GET", "POST"])
def trains():
    if 'firstname' in session:
        return render_template('trains.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('trains.html', navbarname = 'You need to sign in to purchase')





@app.route('/flight_result')
def flight_result():
    if 'firstname' in session:
        return render_template('flight_result.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('flight_result.html')


@app.route('/hotel_result')
def hotel_result():
    if 'firstname' in session:
        return render_template('hotel_result.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('hotel_result.html')



@app.route('/user')
def user():
    if 'firstname' in session and 'lastname' in session:
        firstname = session['firstname']
        lastname = session['lastname']
        return f'<h1>This is your firstname: {firstname} and your last name is: {lastname} :)</h1>'
    else:
        return redirect(url_for('signin'))



@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    #session.pop('_flashes', None)
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        user_session = users.query.filter_by(password = password, email = email).first()
        session['firstname'] = user_session.firstname
        session['lastname'] = user_session.lastname
        session['email'] = user_session.email
        session['id'] = user_session._id # !NEED UNDERSCORE!
        session['status'] = user_session.status
        return redirect(url_for('index'))
    else:
        if 'firstname' in session:
            return redirect(url_for('index'))

        return render_template('signin.html')



@app.route('/signup', methods = ['GET', 'POST'])
def signup():

    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            flash("All fields are required", "error")
            return render_template('signup.html')
            #flash('This is already taken.')
        else:
            user = users(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            #session['firstname'] = users(request.form['firstname'])
            #session['lastname'] = users(request.form['lastname'])
            flash('Registration was successful, you just need to login now.', 'success')
            return redirect(url_for('signin'))
    if request.method == 'GET':
        return render_template('signup.html')



@app.route('/logout')
def logout():
    if 'id' in session:
        session.pop('firstname', None)
        session.pop('lastname', None)
        session.pop('id', None)
        session.pop('email', None)
        flash('Logged out successfully.', 'success')
        return redirect(url_for('signin'))
    else:
        flash('You are not logged in yet.', 'error')
        return redirect(url_for('signin'))




@app.route('/api/processing', methods = ['GET'])
def process_flights():
    if request.method == 'GET':
        user_id = str(session['id'])
        origin_country = request.args.get('origin_country')
        origin_city = request.args.get('origin_city')
        origin_airport = request.args.get('origin_airport')
        date = request.args.get('date')
        time = request.args.get('time')
        destination_country = request.args.get('destination_country')
        destination_city = request.args.get('destination_city')
        destination_airport = request.args.get('destination_airport')
        name = request.args.get('name')
        carrier_id = request.args.get('carrier_id')
        price = request.args.get('price')
        symbol = request.args.get('symbol')
        #user = users.query.filter_by(firstname='ok').first()
        #lastname = session['lastname']

        flight = flights(user_id, carrier_id, price, symbol, origin_airport, destination_airport, date, time)
        db.session.add(flight)
        db.session.commit()
        flash('Ticket added to your cart!', 'success')
        return render_template('flight_result.html',  date = date, time = time, price = price, carrier_id = carrier_id, name = name, symbol = symbol, origin_country = origin_country, origin_city = origin_city, origin_airport = origin_airport, destination_country = destination_country, destination_city = destination_city, destination_airport = destination_city, navbarname = f"Hello {session['firstname']}")
        #return user_id + origin_country + origin_city + origin_airport + date + time + destination_country + destination_city + destination_airport + name + carrier_id + price + symbol
    else:
        flash('An Error occured!', 'error')
        return render_template('flight_result.html',  date = date, time = time, price = price, carrier_id = carrier_id, name = name, symbol = symbol, origin_country = origin_country, origin_city = origin_city, origin_airport = origin_airport, destination_country = destination_country, destination_city = destination_city, destination_airport = destination_city, navbarname = f"Hello {session['firstname']}")


@app.route('/cart')
def cart():
    #flights = flights.query.all()  filter_by(flights._id == session['id'])
    if 'id' in session:
        return render_template('cart.html', flights = flights.query.filter_by(user_id = session['id']).all(), navbarname = f"Hello {session['firstname']}")
    else:
        flash('You need to sign in first', 'error')
        return redirect(url_for('signin'))


@app.route('/troll')
def troll():
    return '<h1 style="text-decoration: underline overline dotted red">HAHA YOU CANT PURCHASE!</h1>'


@app.route('/delete_ticket', methods = ['GET'])
def delete_ticket():
    if request.method == 'GET':
        carrier_id = request.args.get('carrier_id')
        flight = flights.query.filter_by(carrier_id = carrier_id).first()
        db.session.delete(flight)
        db.session.commit()
        flash('Flight was deleted successfully.', 'success')
        return redirect(url_for('cart'))




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)








