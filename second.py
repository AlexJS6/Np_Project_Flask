from flask import Blueprint, render_template

second = Blueprint('second', __name__, static_folder="static", template_folder="templates")

@second.route('/second')
def index():
    return render_template('index.html')