from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from forms import AddForm, DelForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql

app = Flask(__name__)

db = SQLAlchemy(app)

###### MODELS ##########
########################

class Employees(db.Model):

    __tablename__ = "employees"

    emp_id = db.Column(db.StringField, primary_key=True)
    team_lead = db.Column(db.StringField)
    pay_grd = db.Column(db.StringField)
    region = db.Column(db.StringField)

    def __init__(self, emp_id, team_lead, pay_grd, region):
        self.emp_id = emp_id
        self.team_lead = team_lead
        self.pay_grd = pay_grd
        self.region = region








###### PAGES VIEWS ######
#########################

#home page
@app.route('/')
def index():
    return "<h1>text here</h1>"



#page to view info about TractorTek
@app.route('/aboutpage')
def about():
    return "<h2>some text here</h2>"



#page to add sales data
@app.route('/add_sales')
def add_sales():
    return " "



#page to view yearly sales data
@app.route('/sales/<year>')
def sales(year):
    return "<h2> sales data for {} is listed here </h2>".format(year)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(debug=True)