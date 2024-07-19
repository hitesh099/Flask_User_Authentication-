# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from extensions import db
from models import User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('sign_in.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords must match!')
            return redirect(url_for('sign_up'))

        if User.query.filter_by(email=email).first():
            flash('Email address already exists!')
            return redirect(url_for('sign_up'))

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('thank_you'))

    return render_template('sign_up.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')

@app.route('/secretPage', methods=['GET', 'POST'])
def secret_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('secretPage.html')
        else:
            flash('Invalid credentials!')
            return redirect(url_for('index'))
    return render_template('sign_in.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
