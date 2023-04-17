from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warnings
db = SQLAlchemy(app)

#declaring the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    title = db.Column(db.String(80), index = True, unique = True) # book title
    author_name = db.Column(db.String(50), index = True, unique = False) #author name
    author_surname = db.Column(db.String(80), index = True, unique = False) #author surname
    month = db.Column(db.String(20), index = True, unique = False) #the month of book suggestion
    year = db.Column(db.Integer, index = True, unique = False) #the year of book suggestion
    reviews = db.relationship('Review', backref='book', lazy='dynamic') #relationship of Books and Reviews
    
    #Get a nice printout for Book objects
    def __repr__(self):
        return "{} in: {},{}".format(self.title, self.month,self.year)

class Reader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    surname = db.Column(db.String(80), index = True, unique = False)
    email = db.Column(db.String(120), index = True, unique = True)
    reviews = db.relationship('Review', backref = 'reviewer', lazy = 'dynamic')

    #get a nice printout for Reader objects
    def __repr__(self):
        return "Reader: {}".format(self.email)
    
    class Review(db.Model):
        id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
        stars = db.Column(db.Integer, unique = False) #a review's rating
        text = db.Column(db.String(200), unique = False) #a review's text
        book_id = db.Column(db.Integer, db.ForeignKey('book.id')) #foreign key column
        reviewer_id = db.Column(db.Integer, db.ForeignKey('reader.id')) #foreign key column

        #get a nice printout for Review objects
        def __repr__(self):
            return "Review: {} stars: {}".format(self.text, self.stars)
        

@app.route('/')
@app.route('/home')
def home():
    return "Starting App"
