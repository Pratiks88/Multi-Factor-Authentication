# Flask Authentication with Twilio SMS Integration

This is a Flask web application that provides user authentication with Twilio SMS integration for OTP verification. Users can register, login, and reset their passwords using Twilio's SMS service for authentication.

## Technologies Used

- **Framework:** Flask (micro web framework for Python)
- **Database:** SQLite (assumed; consider PostgreSQL or MySQL for production)
- **ORM:** SQLAlchemy (for object-relational mapping)
- **Frontend:** HTML, CSS, JavaScript
- **User Authentication:** Flask-Login
- **SMS Authentication (OTP) Integration:** Twilio
- **Deployment:** [PythonAnywhere](https://www.pythonanywhere.com/)

## Features

- User registration with email, phone number, and password.
- User login with email, password, and OTP verification via SMS.
- Forgot password functionality with OTP verification via SMS for password reset.
- Secure password hashing using passlib's sha256_crypt.
- Session management with Flask's session module.
- Responsive design for mobile and desktop browsers.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo.git
## Install Dependencies

```bash
pip install -r requirements.txt
```
Set up your Twilio account and obtain API credentials.

Update the config.py file with your Twilio API credentials.

Run the application:
```bash
python app.py
```
Access the application in your web browser at http://localhost:5000.
