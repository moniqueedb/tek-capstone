from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField




class AddForm(FlaskForm):
    empid = StringField("Enter Employee Id: ")
    date_of_sale = IntegerField("Product was sold on: ")
    prod_code = StringField("Select Product Code: ")
    submit = SubmitField("Submit")

class DelForm(FlaskForm):
    empid = IntegerField("Enter Employee Id: ")
    date_of_sale = IntegerField("Product was sold on: ")
    prod_code = StringField("Select Product Code: ")
    submit = SubmitField("Remove sale")

#view sales from certain week?