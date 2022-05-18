from math import prod
from tkinter import Y
from xml.sax.handler import property_declaration_handler
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from form import AddProductForm, DelForm, AddWarrantyForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime, ForeignKeyConstraint
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

class ProductInfo(db.Model):

    __tablename__ = "prod_info"

    prod_id = db.Column(db.VARCHAR(10), db.ForeignKey('ProductSales.prod_id'),primary_key=True)
    prod_name = db.Column(db.Text)
    manuf = db.Column(db.Text)
    esp_id = db.Column(db.Text)
    

    def __init__(self, prod_name, prod_manuf, esp_id):
        self.prod_name = prod_name
        self.manuf = prod_manuf
        self.esp_id = esp_id



class ProductSales(db.Model):

    __tablename__ = "prod_sales"

    sales_id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Text, db.ForeignKey('ProductInfo.prod_id'))
    emp_id = db.Column(db.Text, db.ForeignKey('Employees.emp_id'))
    week = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    #__table_args__=(ForeignKeyConstraint([prod_id, emp_id], [ProductInfo.prod_id, Employees.emp_id]), {})


    def __init__(self, prod_id, emp_id, week, year, quantity):
        self.prod_id = prod_id
        self.emp_id = emp_id
        self.week = week
        self.year = year
        self.quantity = quantity

class ProductPrices(db.Model):

    __tablename__ = "prod_prices"

    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Text, db.ForeignKey('ProductSales.prod_id'))
    quarter = db.Column(db.Text)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer)



    def __init__(self, prod_id, quarter):
        self.prod_id = prod_id
        self.quarter = quarter
    

class WarrantySales(db.Model):

    __tablename__ = "warranty_sales"

    sales_id = db.Column(db.Integer, primary_key=True)
    esp_id = db.Column(db.Text, db.ForeignKey('WarrantyPrices.esp_id'))
    emp_id = db.Column(db.Text, db.ForeignKey('Employees.emp_id'))
    week = db.Column(db.Text)
    year = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, esp_id, emp_id, week, quantity):
        self.esp_id = esp_id
        self.emp_id = emp_id
        self.week = week
        self.quantity = quantity

class WarrantyPrices(db.Model):

    __tablename__ = "warranty_prices"

    id = db.Column(db.Integer, primary_key=True)
    esp_id = db.Column(db.VARCHAR(10), db.ForeignKey('WarrantySales.esp_id'))
    price_2020 = db.Column(db.Integer)
    price_2021 = db.Column(db.Integer)

    def __init__(self, esp_id):
        self.esp_id = esp_id


class Employees(db.Model):

    __tablename__ = "employees"

    emp_id = db.Column(db.Text, db.ForeignKey('ProductSales.emp_id'),primary_key=True)
    name = db.Column(db.Text)
    paygrade = db.Column(db.Text)
    region = db.Column(db.Text)

    def __init__(self, emp_id, name, paygrade, region):
        self.emp_id = emp_id
        self.name = name
        self.paygrade = paygrade
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
    return "<h2>TractorTEK is a regional reseller of agricultural equipment based on the US West Coast.</h2>"



#page to add sales data
@app.route('/add_prod', methods=['GET', 'POST'])
def add_prod():
    form = AddProductForm()

    if form.validate_on_submit():

        emp_id = form.emp_id.data
        week = form.week.data
        year = form.year.data
        prod_id = form.prod_id.data
        quantity = form.quantity.data

        new_sale = ProductSales(emp_id, prod_id, week, year, quantity)
        db.session.add(new_sale)
        db.session.commit()
        
        return redirect(url_for(sales_list))


    return render_template('add_prod.html', form=form)



@app.route('/warranties', methods=['GET', 'POST'])
def add_esp():
    form = AddWarrantyForm()

    if form.validate_on_submit():

        emp_id = form.emp_id.data
        week = form.week.data
        year = form.year.data
        esp_id = form.esp_id.data
        quantity = form.quantity.data

        new_esp = WarrantySales(emp_id, esp_id, week, year, quantity)
        db.session.add(new_esp)
        db.session.commit()
        
        return redirect(url_for(sales_list))


    return render_template('add_esp.html', form=form)



#page to delete sales data
@app.route('/delete')
def del_sales():
    form = DelForm()
    return render_template('del_sales.html', form=form)





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