from flask import Flask, render_template, url_for, redirect,flash                                                  #templates and linking functions to go to other pages.
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user,current_user           #login logout functionalities
from flask_wtf import FlaskForm                                                                                    #used to take user information and put into database
from wtforms import StringField, PasswordField, SubmitField,validators,IntegerField,TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Length, ValidationError,Optional
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate                                                                                    #for encryption of password
import mysql.connector
from datetime import date




mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "Tweety2002**",
  database = "DBMSP"
)


app = Flask(__name__)                                                                                               #name of flask object
db = SQLAlchemy(app)                                                                                                #database object
bcrypt=Bcrypt(app) 
migrate=Migrate(app,db)                                                                                                 #encryption object
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tweety2002**@localhost/DBMSP'                         #database configuration including mysql username,password, and the name of the database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'                                                    #sqlite3 database configuration
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader                                                                                          #checks the db for the login credentials
def load_user(user_username):
    return User.query.get(str(user_username))


class User(db.Model, UserMixin):
    __tablename__='User'
    Fname=db.Column(db.String(20),nullable=False)
    Lname=db.Column(db.String(20))
    Email_ID=db.Column(db.String(40),unique=True)
    Age=db.Column(db.Integer,nullable=False)
    Country=db.Column(db.String(15),server_default='India',nullable=False)                                                                      #user table in the users database including id, username, and password
    username = db.Column(db.String(20), nullable=False, primary_key=True)
    psw = db.Column(db.String(80), nullable=False)
    rev=db.relationship('Reviews', backref='user')
    def get_id(self):
           return (self.username)


class Book(db.Model):
    __tablename__='Book'
    B_ID=db.Column(db.Integer, primary_key=True,autoincrement=False)
    Book_Name=db.Column(db.String(40) , nullable=False)
    Author=db.Column(db.String(30))
    Pub_Year=db.Column(db.Integer())
    Pub_Name=db.Column(db.String(30))
    Rating=db.Column(db.Integer)
    bb=db.relationship('Reviews', backref='book')


class Movie(db.Model):
    __tablename__='Movie'
    M_ID=db.Column(db.Integer, primary_key=True,autoincrement=False)
    Mov_Name=db.Column(db.String(40) , nullable=False)
    Director=db.Column(db.String(30))
    Mov_date=db.Column(db.Date)
    Rating=db.Column(db.Integer)
    mm=db.relationship('Reviews', backref='movie')
    


class Documentary(db.Model):
    __tablename__='Documentary'
    D_ID=db.Column(db.Integer, primary_key=True,autoincrement=False)
    Doc_Name=db.Column(db.String(40) , nullable=False)
    Director=db.Column(db.String(30))
    Release_date=db.Column(db.Date)
    Rating=db.Column(db.Integer)
    dd=db.relationship('Reviews',backref='documentary')
    


class Reviews(db.Model,UserMixin):
    __tablename__='Reviews'
    Review_ID=db.Column(db.Integer,primary_key=True)
    Rev_Title=db.Column(db.String(30))
    Rev_date=db.Column(db.Date)
    Movie_ID=db.Column(db.Integer,db.ForeignKey('Movie.M_ID', ondelete="CASCADE"))
    Doc_ID=db.Column(db.Integer, db.ForeignKey('Documentary.D_ID', ondelete="CASCADE"))
    Book_ID=db.Column(db.Integer, db.ForeignKey('Book.B_ID', ondelete="CASCADE"))
    Username=db.Column(db.String(20), db.ForeignKey('User.username', ondelete="CASCADE"))
    content=db.Column(db.String(2000))



class RegisterForm(FlaskForm):            
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    psw = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    Fname = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "First Name"})
    Lname = StringField(validators=[
                            Length(min=4, max=20)], render_kw={"placeholder": "Last Name"})
    Email_ID = StringField(validators=[
                            InputRequired(), Length(min=10, max=50)], render_kw={"placeholder": "Email Id"})
    Country = StringField(Optional(strip_whitespace=True), render_kw={"placeholder": "Country"} )
    Age = IntegerField(validators=[InputRequired(),validators.NumberRange(min=18, max=1000)])
    submit = SubmitField('Register')


    def validate_username(self, username):                                                                                               #function used to check whether the username is already in the db or not
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):                                                                                               #entering the login credentials into the form provided with min and max characters to each field
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    psw = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')                                                                                         #tells that this form will be in the login html page and the details will be submitted to the login page
    
                                                                                     
    
class ReviewForm(FlaskForm):
    Rev_Title=StringField(validators=[
        InputRequired(), Length(min=5,max=200)],render_kw={"placeholder":"Enter the title of your Review!"})

    Book_ID=IntegerField(Optional(strip_whitespace=True),render_kw={"placeholder":"Enter the ID of the book you chose!"})

    Movie_ID=IntegerField(Optional(strip_whitespace=True),render_kw={"placeholder":"Enter the ID of the movie you chose!"})

    Doc_ID=IntegerField(Optional(strip_whitespace=True),render_kw={"placeholder":"Enter the ID of the documentary you chose!"})

    content=TextAreaField(validators=[InputRequired()],widget=TextArea(), render_kw={"placeholder":"Enter your Review!"})

    submit=SubmitField('Submit')


@app.route('/')                                                                                                           #main page
def home():
    return render_template('home.html') 

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():                                                                                      #checks if login info is valid
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.psw,form.psw.data):
                login_user(user)
                return redirect(url_for('dashboard')) # after logging in redirects to the dashboard page
    return render_template('login.html',form=form)


@app.route('/dashboard', methods=['GET', 'POST'])    #page after logging in 
@login_required  #specifies that this page can only be accesssed after logging in
def dashboard():
    uss=current_user.username
    info=User.query.filter_by(username=uss).first()
    return render_template('dashboard.html',info=info)



@app.route('/Books', methods=['GET', 'POST'])    #page after logging in 
@login_required  #specifies that this page can only be accesssed after logging in
def Books():
    return render_template('Books.html')

@app.route('/Movies', methods=['GET', 'POST'])    #page after logging in 
@login_required  #specifies that this page can only be accesssed after logging in
def Movies():
    return render_template('Movies.html')


@app.route('/Documentary', methods=['GET', 'POST'])    #page after logging in 
@login_required  #specifies that this page can only be accesssed after logging in
def Documentaries():
    return render_template('Documentary.html')



@app.route('/logout', methods=['GET', 'POST']) #takes user to login page after logging out
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.Country.data==None:
        form.Country.data='India'
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.psw.data)
        new_user = User(username=form.username.data, psw=hashed_password,Fname=form.Fname.data,Lname=form.Lname.data, Age=form.Age.data, Country=form.Country.data, Email_ID=form.Email_ID.data)   #hashes the 
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/reviewstat',methods=['GET','POST'])
@login_required
def reviewstat():
    curs=mydb.cursor()
    curs.execute("select user.fname,count(reviews.username) from user,reviews where user.username=reviews.username group by user.username")
    data=curs.fetchall()
    #curs.execute(" create view medata1 as select b_id,m_id,d_id, count(*) from book,movie,documentary,reviews where b_id=Book_id and m_id=movie_id and d_id=doc_id group by b_id,m_id,d_id")
    curs.execute("select * from medata1")
    data2=curs.fetchall()
    #curs.execute("select user.fname, reviews.content from user,reviews where user.username=reviews.username")
    #data3=curs.fetchall()
    curs.execute("select * from book where b_id!=0")
    data4=curs.fetchall()
    curs.execute("select * from movie where m_id!=0")
    data5=curs.fetchall()
    curs.execute("select * from documentary where d_id!=0")
    data6=curs.fetchall()
    return render_template('reviewstat.html',data=data,data2=data2,data4=data4,data5=data5,data6=data6)



@app.route('/review',methods=['GET','POST'])
@login_required 
def review():
    form=ReviewForm()
    if form.validate_on_submit():
        use=current_user.username
        tdate=date.today()
        new_review=Reviews(Username=use,Rev_Title=form.Rev_Title.data,Book_ID=form.Book_ID.data,Rev_date=tdate,Movie_ID=form.Movie_ID.data, Doc_ID=form.Doc_ID.data,content=form.content.data)
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('review.html',form=form)


@app.route('/DispRev')
@login_required
def DispRev():
    
    revs=Reviews.query.order_by(Reviews.Review_ID)
    return render_template('DispRev.html',posts=revs)


if __name__ == "__main__":   #to run the app
    app.run(debug=True)