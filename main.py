from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from passlib.hash import sha256_crypt
from twilio.rest import Client
import secrets  # For generating a random security token
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site9.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key for session management
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    security_token = db.Column(db.String(10), nullable=False)
    otp = db.Column(db.String(6), nullable=True)

# Index or Home page
@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', name=session['user']['name'])
    return redirect(url_for('login'))

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']
        security_token = request.form['security_token']

        # Hash the password before storing
        hashed_password = sha256_crypt.hash(password)

        # Create a new user
        new_user = User(name=name, email=email, number=number, password=hashed_password, security_token=security_token)

        try:
            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            # Store user information in the session
            session['user'] = {'name': name, 'email': email, 'number': number}

            return redirect(url_for('home'))
        except IntegrityError:
            # If user with the same email or number already exists, show an error
            db.session.rollback()
            flash("User with this email or number already exists. Please choose a different email or number.", "error")

    return render_template('register.html')

# Login Page
# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database to check if the user exists
        user = User.query.filter_by(email=email).first()

        if user and sha256_crypt.verify(password, user.password):
            # Generate a 6-digit OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Store OTP and user information in the session
            session['otp'] = otp
            session['user'] = {'name': user.name, 'email': user.email, 'number': user.number}
            user.otp = otp
            db.session.commit()

            # Send the OTP to the user's registered number using Twilio
            send_otp_to_user(user.number, otp)

            # Redirect to the verify_otp route
            return redirect(url_for('verify_otp'))

        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)

    return render_template('login.html')


def send_otp_to_user(phone_number, otp):
    # Your Twilio account SID, auth token, and Twilio phone number
    account_sid = 'ACcc63f4476ec4b42fe0ceb3d61ba9bad9'
    auth_token = '498fdb368b2eb905c18da9a7068a0454'
    twilio_phone_number = '+14694163905'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the OTP to the user's phone number
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=twilio_phone_number,
        to=phone_number
    )
    print(f"OTP Sent to {phone_number}. Message SID: {message.sid}")

# Verify OTP Page
# Verify OTP Page
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'otp' not in session or 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if entered_otp == session['otp']:
            # Clear the OTP from the session
            session.pop('otp', None)

            # Update the user information in the session
            user = User.query.filter_by(email=session['user']['email']).first()
            session['user'] = {'name': user.name, 'email': user.email, 'number': user.number}

            return redirect(url_for('home'))
        else:
            error = 'Invalid OTP. Please try again.'
            return render_template('verify_otp.html', error=error)

    return render_template('verify_otp.html')



# Forgot Password Page
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        security_token = request.form['security_token']

        # Query the database to check if the user exists
        user = User.query.filter_by(email=email, security_token=security_token).first()

        if user:

            session['user'] = {'name': user.name, 'email': user.email, 'number': user.number}
            return redirect(url_for('home'))
        else:
            error = 'Invalid email or security token. Please try again.'
            return render_template('forgot_password.html', error=error)

    return render_template('forgot_password.html')


# Logout
@app.route('/logout')
def logout():
    # Clear user information from the session
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
