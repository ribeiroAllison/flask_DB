from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

#declaring the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column
    title = db.Column(db.String(80), index = True, unique = True) 
    author_name = db.Column(db.String(50), index = True, unique = False)
    author_surname = db.Column(db.String(80), index = True, unique = False) 
    month = db.Column(db.String(20), index = True, unique = False) 
    year = db.Column(db.Integer, index = True, unique = False) 
    reviews = db.relationship('Review', backref = 'book', lazy = 'dynamic') 
    
    #Get a nice printout for Book objects
    def __repr__(self):
        return "{} in: {},{}".format(self.title, self.month, self.year)

#Declaring the Reader model
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    surname = db.Column(db.String(80), unique = False, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    reviews = db.relationship('Review', backref='reviewer', lazy = 'dynamic')
  
    #get a nice printout for Reader objects
    def __repr__(self):
        return "Reader: {}".format(self.email)

#declaring the Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, 
    stars = db.Column(db.Integer, unique = False) #a review's rating
    text = db.Column(db.String(200), unique = False) #a review's text
    book_id = db.Column(db.Integer, db.ForeignKey('book.id')) #foreign key 
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reader.id'))

    #get a nice printout for Review objects
    def __repr__(self):
        return "Review: {} stars: {}".format(self.text, self.stars)

#declaring the Annotation model
class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), unique = False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reader.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    
    def __repr__(self):
        return '<Annotation {}-{}:{} >'.format(self.reviewer_id, self.book_id, self.text)

#some routing for displaying the home page
@app.route('/')
@app.route('/home')
def home():
    return "Start"

