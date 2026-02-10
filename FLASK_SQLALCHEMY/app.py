from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Student(db.Model):
    roll_no=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String[200],nullable=False)
    marks=db.Column(db.String[200],nullable=False)

with app.app_context():
    db.create_all()