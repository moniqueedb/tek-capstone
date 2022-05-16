from flask import Flask, render_template

app = Flask(__name__)

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