from email.utils import format_datetime, formatdate
from sqlite3 import Date
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField, DateField




class AddProductForm(FlaskForm):
    emp_id = StringField("Enter Employee Id: ")
    week = StringField("Week of Sale: ")
    year = DateField("Year: ", format="%Y")
    prod_id = StringField("Select Product Code: ")
    quantity = IntegerField("Quantity of Products Sold: ")
    submit = SubmitField("Submit")

class AddWarrantyForm(FlaskForm):
    emp_id = StringField("Enter Employee Id: ")
    esp_id = StringField("Extended Service Plan Code: ")
    week = StringField("Week of Sale: ")
    year = DateField("Year: ")
    quantity = IntegerField("Quantity of Warranties Sold: ")
    submit = SubmitField("Submit")

class DelForm(FlaskForm):
    emp_id = IntegerField("Enter Employee Id: ")
    date = IntegerField("Product was sold on: ")
    prod_id = StringField("Select Product Code: ")
    submit = SubmitField("Remove sale")

#view sales from certain week?