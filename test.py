from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(hours = 24)


db = SQLAlchemy(app)

def format_response(flight):
    pass



@app.route('/')
def get_flights():
    country = 'US'
    currency = 'USD'
    locale = 'en-US'
    originplace = 'SFO-sky'
    destinationplace = 'JFK-sky'
    date = '2019-09-01'

    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/{country}/{currency}/{locale}/{originplace}/{destinationplace}/{date}"

    querystring = {"inboundpartialdate":"2019-12-01"}

    headers = {
        'x-rapidapi-key': "089d02225bmshefa31c6ca5f2456p154c11jsnebd679e760b4",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response)



@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        return redirect(url_for('user'))
    else:
        if 'email' in session:
            return redirect(url_for('user'))

        return render_template('signin.html')




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)