from flask import Flask, jsonify, render_template, request, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.secret_key = "secret_key" # Change this to a random secret key
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Student(db.Model):
    roll_no=db.Column(db.Integer,primary_key=True)
    photo=db.Column(db.LargeBinary,nullable=False)
    name=db.Column(db.String(200),nullable=False)
    marks=db.Column(db.String(200),nullable=False)

class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(200),nullable=False)

with app.app_context():
    db.create_all()

@app.route('/admin_add',methods=['GET','POST'])
def admin_add():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin=Admin(username=username,password=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        flash('Admin added successfully', 'success')
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=Admin.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            session['logged_in']=True
            session['username']=username
            flash('You were successfully logged in','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password','danger')
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were successfully logged out', 'info')

    return redirect(url_for("login"))

@app.route('/home',methods=['GET','POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method=='POST':
        rno=request.form['roll_no']
        p=request.files.get('photo')
        n=request.form['name']
        m=request.form['marks']
        p_data=p.read() if p else None
        new_student=Student(roll_no=rno,photo=p_data,name=n,marks=m)
        db.session.add(new_student)
        db.session.commit()
    
    return render_template('index.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method=="POST":
        rno=request.form['roll_no']
        n=request.form['name']
        m=request.form['marks']
        student=Student.query.filter_by(roll_no=rno).first()
        if student:
            student.name=n
            student.marks=m
            db.session.add(student)
            db.session.commit()

    return render_template('update.html')

@app.route('/delete',methods=['GET','POST'])
def delete():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method=="POST":
        rno=request.form['roll_no']
        student=Student.query.filter_by(roll_no=rno).first()
        if student:
            student.roll_no=rno
            db.session.delete(student)
            db.session.commit()
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)