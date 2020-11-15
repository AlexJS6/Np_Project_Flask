from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flights')
def flights():
    return render_template('flights.html')

@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('user', email = email, pwd = password))
    else:
        return render_template('signin.html')

@app.route('/<email>/<pwd>')
def user(email, pwd):
    return f'<h1>Email: {email}, Password: {pwd}</h1>'

@app.route('/signup')
def signup():
        return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)