'''from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
import requests


session = session('session', __name__, static_folder="static", template_folder="templates")


@session.route('/signin', methods = ['POST', 'GET'])
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


@session.route('/signup')
def signup():
        return render_template('signup.html')


@session.route('/logout')
def logout():
    if 'email' in session:
        email = session['email']
        flash(f'You have been logged out successfully: {email}', 'info')
    session.pop('email', None)
    return redirect(url_for('signin'))'''