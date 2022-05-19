from math import prod
from tkinter import Y
from xml.sax.handler import property_declaration_handler
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from form import AddProductForm, DelForm, AddWarrantyForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime, ForeignKeyConstraint, ForeignKey
import pymysql
import mysql.connector

app = Flask(__name__)

app.config['SECRET_KEY'] = "my secret key"

engine ='mysql+pymysql://root:pw123@localhost/tractortek'

app.config['SQLALCHEMY_DATABASE_URI'] = engine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###### MODELS ##########
########################

SET_GLOBAL_FOREIGN_KEY_CHECKS=0

class ProductInfo(db.Model):

    __tablename__ = "prod_info"

    prod_id = db.Column(db.VARCHAR(8),primary_key=True)
    prod_name = db.Column(db.VARCHAR(30))
    manuf = db.Column(db.VARCHAR(30))
    esp_id = db.Column(db.VARCHAR(8))
    

    def __init__(self, prod_name, prod_manuf, esp_id):
        self.prod_name = prod_name
        self.manuf = prod_manuf
        self.esp_id = esp_id


class Employees(db.Model):

    __tablename__ = "employees"

    emp_id = db.Column(db.VARCHAR(10),primary_key=True)
    name = db.Column(db.VARCHAR(30))
    paygrade = db.Column(db.VARCHAR(5))
    region = db.Column(db.VARCHAR(2))

    def __init__(self, emp_id, name, paygrade, region):
        self.emp_id = emp_id
        self.name = name
        self.paygrade = paygrade
        self.region = region



class ProductSales(db.Model):

    __tablename__ = "prod_sales"


    sales_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Text, ForeignKey('prod_info.prod_id'))
    emp_id = db.Column(db.Text, ForeignKey('employees.emp_id'))
    week = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    #__table_args__=(ForeignKeyConstraint([prod_id, emp_id], [ProductInfo.prod_id, Employees.emp_id]), {})


    def __init__(self, emp_id, prod_id, week, year, quantity):
        self.emp_id = emp_id
        self.prod_id = prod_id
        self.week = week
        self.year = year
        self.quantity = quantity

class WarrantySales(db.Model):

    __tablename__ = "warranty_sales"

    sales_id = db.Column(db.Integer, primary_key=True)
    esp_id = db.Column(db.VARCHAR(8), ForeignKey('warranty_prices.esp_id'))
    emp_id = db.Column(db.VARCHAR(10), ForeignKey('employees.emp_id'))
    week = db.Column(db.VARCHAR(5))
    year = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, esp_id, emp_id, week, year, quantity):
        self.esp_id = esp_id
        self.emp_id = emp_id
        self.week = week
        self.year = year
        self.quantity = quantity


class ProductPrices(db.Model):

    __tablename__ = "prod_prices"

    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Text, ForeignKey('ProductSales.prod_id'))
    quarter = db.Column(db.Text)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)



    def __init__(self, prod_id, quarter):
        self.prod_id = prod_id
        self.quarter = quarter
    

class WarrantyPrices(db.Model):

    __tablename__ = "warranty_prices"

    id = db.Column(db.Integer, primary_key=True)
    esp_id = db.Column(db.VARCHAR(10), ForeignKey('warranty_sales.esp_id'))
    price_2020 = db.Column(db.Integer)
    price_2021 = db.Column(db.Integer)

    def __init__(self, esp_id):
        self.esp_id = esp_id




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
    return "<h2>TractorTEK is a regional reseller of agricultural equipment based on the US West Coast.</h2>"



#page to add sales data
@app.route('/add_prod', methods=['GET', 'POST'])
def add_prod():
    form = AddProductForm()

    if form.validate_on_submit():

#organize order
        emp_id = form.emp_id.data
        week = form.week.data
        year = form.year.data
        prod_id = form.prod_id.data
        quantity = form.quantity.data

        new_sale = ProductSales(emp_id, prod_id, week, year, quantity)
        db.session.add(new_sale)
        db.session.commit()
        
        return redirect(url_for('index'))


    return render_template('add_prod.html', form=form)



@app.route('/warranties', methods=['GET', 'POST'])
def add_esp():
    form = AddWarrantyForm()

    if form.validate_on_submit():

        emp_id = form.emp_id.data
        esp_id = form.esp_id.data
        week = form.week.data
        year = form.year.data
        quantity = form.quantity.data

        new_esp = WarrantySales(emp_id, esp_id, week, year, quantity)
        db.session.add(new_esp)
        db.session.commit()
        
        return redirect(url_for('index'))


    return render_template('add_esp.html', form=form)





#page to view yearly sales data
@app.route('/list')
def sales_list():

    allsales = ProductSales.query.all()
    #tt_warrsales = WarrantySales.query.all()

    return render_template('sales_list.html', allsales=allsales)





@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(debug=True)