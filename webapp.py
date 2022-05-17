from math import prod
from xml.sax.handler import property_declaration_handler
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from form import AddForm, DelForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = "my secret key"

engine ='mysql+pymysql://root:pw123@localhost/tractortek'

app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###### MODELS ##########
########################

class Main(db.Model):

    __tablename__ = "tt_main"

    prod_id = db.Column(db.Text, primary_key=True)
    esp_id = db.Column(db.Text)

    def __init__(self, prod_id, esp_id):
        self.prod_id = prod_id
        self.esp_id = esp_id

class ProductInfo(db.Model):

    __tablename__ = "prod_info"

    prod_id = db.Column(db.Text, primary_key=True)
    prod_name = db.Column(db.Text)
    manuf = db.Column(db.Text)
    esp_id = db.Column(db.Text)

    def __init__(self, prod_id, prod_name, prod_manuf, esp_id):
        self.prod_id = prod_id
        self.prod_name = prod_name
        self.manuf = prod_manuf
        self.esp_id = esp_id


class ProductSales(db.model):

    __tablename__ = "prod_sales"

    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Text, db.ForeignKey('prod_info'))
    emp_id = db.Column(db.Text)
    week_num = db.Column(db.Text)
    year = db.Column(db.Integer)
    quant_sold = db.Column(db.Integer)

    def __init__(self, prod_id, emp_id, week_num, year, quant_sold):
        self.prod_id = prod_id
        self.emp_id = emp_id
        self.week_num = week_num
        self.year = year
        self.quant_sold = quant_sold

class ProductPrices(db.Model):

    __tablename__ = "prod_prices"

    prod_id = db.Column(db.Text)
    quarter = db.Column(db.Text)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, prod_id, quarter):
        self.prod_id = prod_id
        self.quarter = quarter
    

class WarrantySales(db.Column):

    __tablename__ = "warranty_sales"

    esp_id = db.Column(db.Text, primary_key=True)
    emp_id = db.Column(db.Text)
    week_num = db.Column(db.Text)
    year = db.Column(db.Integer)
    quant_sold = db.Column(db.Integer)

    def __init__(self, esp_id, emp_id, week_num):
        self.esp_id = esp_id
        self.emp_id = emp_id
        self.week_num = week_num

class WarrantyPrices(db.Model):

    __tablename__ = "warranty_prices"

    esp_id = db.Column(db.Text)
    price_2020 = db.Column(db.Integer)
    price_2021 = db.Column(db.Integer)

    def __init__(self, esp_id):
        self.esp_id = esp_id


class Employees(db.Model):

    __tablename__ = "employees"

    emp_id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    pay_grd = db.Column(db.Text)
    region = db.Column(db.Text)

    def __init__(self, emp_id, name, pay_grd, region):
        self.emp_id = emp_id
        self.name = name
        self.pay_grd = pay_grd
        self.region = region


db.create_all()


###### PAGES VIEWS ######
#########################

#home page
@app.route('/')
def index():
    return render_template('index.html')



#page to view info about TractorTek
@app.route('/aboutpage')
def about():
    return "<h2>some text here</h2>"



#page to add sales data
@app.route('/add_sales')
def add_sales():
    form = AddForm()

    #if form.validate_on_submit()


    return render_template('add_sales.html', form=form)



#page to delete sales data
@app.route('/delete')
def del_sales():
    form = DelForm()
    return render_template('del_sales.html', form=form)





#page to view yearly sales data
@app.route('/list')
def sales_list():

    return render_template('sales_list.html')





@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(debug=True)