from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv("PersonalSite/.env")

# initialize flask application
app = Flask(__name__)
app.secret_key = os.getenv('app_key')
server = app

# Function to convert environment variable to boolean
def str_to_bool(value):
    return value.lower() in ['true', '1', 'yes']

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('server')
app.config['MAIL_PORT'] = int(os.getenv('port'))
app.config['MAIL_USE_TLS'] = str_to_bool(os.getenv('tls_setting'))
app.config['MAIL_USE_SSL'] = str_to_bool(os.getenv('ssl_setting'))
app.config['MAIL_USERNAME'] = os.getenv('from_email')
app.config['MAIL_PASSWORD'] = os.getenv('password')
app.config['MAIL_DEFAULT_SENDER'] = ('Personal Site Contact form message', os.getenv('from_email'))

mail = Mail(app)

# home screen route
@app.route("/")
def run_website():
    return render_template("index.html")

# Route to handle email sending
@app.route("/send_email", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if not name or not email or not message:
        flash("All fields are required.", 'error')
        return redirect(url_for("run_website"))

    msg = Message(
        subject="New Contact Form Submission",
        recipients=[os.getenv("recipient")],  
        body=f"Name: {name}\nEmail: {email}\nMessage: {message}"
    )
    try:
        mail.send(msg)
        flash("Message sent successfully!")
    except Exception as e:
        print(f"Exception{str(e)}, no message sent")
        print(os.getenv('server'))
        print(str_to_bool(os.getenv('ssl_setting'), type(str_to_bool(os.getenv('ssl_setting')))))
        print(int(os.getenv('port')), type(int(os.getenv('port'))))
        flash(f"An error occurred: {str(e)}", 'error')

    return redirect(url_for("run_website"))


if __name__ == "__main__":
    app.run(debug=True)
