import os

from datetime import datetime
from dotenv import load_dotenv
from urllib.parse import urljoin
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask import Flask, render_template, request, redirect, url_for, flash

# Load env vars
load_dotenv()

# App config
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['CDN_DOMAIN'] = os.environ.get('CDN_DOMAIN')
Bootstrap(app)


# Connect to db
DB_URL = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL.replace('postgres://', 'postgresql://') if DB_URL else 'sqlite:///notfromparis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure models for db
class EmailResponse(db.Model):
    __tablename__ = 'email_responses'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    time_created = db.Column(db.DateTime(), default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.template_global()
def get_cdn_url(filename):
    """Grab CDN URL to grab static files"""
    static_url = app.config.get('CDN_DOMAIN')

    if static_url:
        return urljoin(static_url, filename)

    return url_for('static', filename=filename)

@app.route('/')
def home():
    """Render home page"""
    return render_template('index.html')

@app.route('/press-kit')
def pressKit():
    """Render press kit page"""
    return render_template('pressKit.html')   

@app.route('/register', methods=['POST'])
def register():
    """Register an email"""
    if request.method == 'POST':
        # Get email from form and create db record
        new_email_response = EmailResponse(email = request.form.get('email'))        
        # Commit to db
        try:
            db.session.add(new_email_response)
            db.session.commit()
            # Thank you message
            flash("WELCOME,i'm glad you're here")
        except exc.IntegrityError:
            flash("WELCOME BACK,looks like you're already signed up")
        # Return to home page
        return redirect(url_for('home'))
    # If this errors for any reason, return to home page
    return render_template('index.html') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)
