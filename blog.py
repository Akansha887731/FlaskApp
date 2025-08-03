from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import RegistrationForm, LoginForm

app = Flask(__name__)

# >>> import secrets
# >>> print(secrets.token_hex(16))

app.config['SECRET_KEY'] = '758c54a8716326fbd0d583646d69dbbb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return(f"User ('{self.username}', '{self.email}', '{self.image_file}')")
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(f"Post ('{self.title}', '{self.date_posted}')")


posts = [{
    'title': "My Blog 1",
    'content': "This is my first blog post. Welcome to my blog!",
    'author': "John Doe",
    'date_posted': "October 1, 2023"},
    {
    'title': "My Blog 2",
    'content': "This is my second blog post. Hope you enjoy reading!",  
    'author': "Jane Smith",
    'date_posted': "August 15, 2023"},
    ]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='Home Page')


@app.route('/about')
def about():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register Page', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'akansha887731@gmail.com' and form.password.data == '1234567':
            flash("Login successful!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login failed. Please check your credentials.", 'danger')

    return render_template('login.html', title='Login Page', form=form)

if __name__ == '__main__':

    app.run(debug=True, port=5000)
    
