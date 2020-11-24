from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_mail import Mail, Message
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

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


@app.route('/email_processing')
def email_processing():
    if 'email' in session:
        msg = Message('Vector password reset', sender = 'VectorNpProject@gmail.com', recipients= [session['email']])
        msg.body = f"Hello {session['firstname']} {session['lastname']}!"
        mail.send(msg)
        flash('password sent, look at your emails')
        return render_template('change_profile.html', firstname = session['firstname'], lastname = session['lastname'], email = session['email'])
    else:
        redirect(url_for('index'))




'''@app.route('/flight', methods = ['POST', 'GET'])
def api():
    if request.method == 'GET':
        country = request.args.get('country')
        currency = request.args.get('currency')
        locale = request.args.get('locale')
        originplace = request.args.get('originplace')
        destinationplace = request.args.get('destinationplace')
        outboundpartialdate = request.args.get('outboundpartialdate')

        url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{outboundpartialdate}"
    
        querystring = {"inboundpartialdate":"2019-12-01"}
        
        headers = {
        'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

        departure_date =  str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['OutboundLeg']['DepartureDate'])
        price = str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])
        return f'Hello the price is {price} and you leave the {departure_date}'
        #return str(requests.request("GET", url, headers=headers, params = querystring).json()['Quotes'][0]['MinPrice'])'''
      

 



class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key = True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


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





@app.route('/show_test')
def show_all():
    return render_template('show_all.html', users = users.query.all())

@app.route('/', methods = ['GET', 'POST'])
def index():
    '''if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            return redirect(url_for('signup'))
        else:
            user = users(request.form['password'], request.form['email'], request.form['lastname'], request.form['firstname'])
            db.session.add(user)
            db.session.commit()
            #flash(f'Welcome {user[0]}!')
            return redirect(url_for('show_all'))'''
    if 'firstname' in session:
        return render_template('index.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('index.html', navbarname = 'You need to sign in to purchase')



@app.route('/car', methods = ['GET', 'POST'])
def car():
    if 'firstname' in session:
        return render_template('cars.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('cars.html', navbarname = 'You need to sign in to purchase')





@app.route('/change_profile')
def change_profile():
    if 'firstname' in session:
        user = users.query.filter_by(firstname = session['firstname'], lastname = session['lastname']).first()
        firstname = user.firstname
        lastname = user.lastname
        email = user.email
        password = user.password
        return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email, password = password)
    else:
        redirect(url_for('signin'))


@app.route('/change_profile_processing', methods = ['POST'])
def change_profile_processing():
    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email']:
            user = users.query.filter_by(firstname = session['firstname'], lastname = session['firstname']).first()
            session.pop('_flashes', None)
            flash('All fields are required.')
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
            flash('Changes done successfully')
            return render_template('change_profile.html', firstname = firstname, lastname = lastname, email = email)


@app.route('/trains', methods = ["GET", "POST"])
def trains():
    if 'firstname' in session:
        return render_template('trains.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('trains.html', navbarname = 'You need to sign in to purchase')




@app.route('/autobus', methods = ['GET', 'POST'])
def autobus():
    if 'firstname' in session:
        return render_template('autobus.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('autobus.html', navbarname = 'You need to sign in to purchase')



@app.route('/flight_result')
def flight_result():
    if 'firstname' in session:
        return render_template('flight_result.html', navbarname = f"Hello {session['firstname']}")
    else:
        return render_template('flight_result.html', navbarname = 'You need to sign in to purchase')



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
        return redirect(url_for('index'))
    else:
        if 'firstname' in session:
            return redirect(url_for('index'))

        return render_template('signin.html')



@app.route('/signup', methods = ['GET', 'POST'])
def signup():

    if request.method == 'POST':
        if not request.form['firstname'] or not request.form['lastname'] or not request.form['email'] or not request.form['password'] or not request.form['passwordconfirm']:
            flash('All fields are required.')
            return render_template('signup.html')
            #flash('This is already taken.')
        else:
            user = users(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'])
            db.session.add(user)
            db.session.commit()
            #session['firstname'] = users(request.form['firstname'])
            #session['lastname'] = users(request.form['lastname'])
            flash('Registration was successful, you just need to login now.')
            return redirect(url_for('signin'))
    if request.method == 'GET':
        return render_template('signup.html')



@app.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
        flash(f'You have been logged out successfully: {email}', 'info')
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('id', None)
    session.pop('email', None)
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
        flash('Ticket added to your cart!')
        return render_template('flight_result.html',  date = date, time = time, price = price, carrier_id = carrier_id, name = name, symbol = symbol, origin_country = origin_country, origin_city = origin_city, origin_airport = origin_airport, destination_country = destination_country, destination_city = destination_city, destination_airport = destination_city)
        #return user_id + origin_country + origin_city + origin_airport + date + time + destination_country + destination_city + destination_airport + name + carrier_id + price + symbol
    else:
        flash('An Error occured!')
        return render_template('flight_result.html',  date = date, time = time, price = price, carrier_id = carrier_id, name = name, symbol = symbol, origin_country = origin_country, origin_city = origin_city, origin_airport = origin_airport, destination_country = destination_country, destination_city = destination_city, destination_airport = destination_city)


@app.route('/cart')
def cart():
    #flights = flights.query.all()  filter_by(flights._id == session['id'])

    return render_template('cart.html', flights = flights.query.filter_by(user_id = session['id']).all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)








