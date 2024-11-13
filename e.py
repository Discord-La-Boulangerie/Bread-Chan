from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Replace with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# Initialize the database
db.create_all()

# Example usage
user = User(username='john_doe', email='john.doe@example.com',
            password='password123')
db.session.add(user)
db.session.commit()

users = User.query.all()
for user in users:
    print(user.username, user.email)
