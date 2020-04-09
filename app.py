#Importing
#import filename
#from filename import.....

from flask import Flask,render_template,request,redirect,url_for

import pygal
from datetime import datetime, timedelta

#calling/instaciating

app = Flask(__name__)

#creating endpoints/routes
#1.declaration of a route
#2.a function embeded to the route

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact us')
def contact_us():
    return render_template("contact.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/inventories', methods=['GET' , 'POST'])
def inventories():

    if request.method == 'POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']
        

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)


       
        return redirect( url_for ('inventories'))


    return render_template("inventories.html")


@app.route('/add_stock', methods=['POST'])
def add_stock():
    if request.method=='POST':
         stock = request.form['stock']
    print(stock)
    return redirect( url_for ('inventories'))


@app.route('/add_sale', methods=['POST'])
def add_sale():
    if request.method == 'POST':
        quantity = request.form['quantity']
    print(quantity)
    return redirect(url_for ('inventories'))

@app.route('/edit_inventory',methods=['POST'])
def edit_inventory():
    if request.method == 'POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)

        return redirect( url_for ('inventories'))
    
@app.route('/data_visualisation')
def data_visualisation():
    
    pie_chart = pygal.Pie()

    my_pie_data = [
        ('Nairobi', 63),
        ('Mombasa', 20),
        ('Kilifi', 17),
        ('Machakos', 30),
        ('Kiambu', 7)
    ]
    for each in my_pie_data:
        pie_chart.add(each[0],each[1])
    
    pie_data = pie_chart.render_data_uri()




    #end of pie chart

    #start of line graph
    
    '''line_chart.title='Browser usage evolution (in %)'
    line_chart.x_labels= map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])'''

    data = [
        {'month': 'January', 'total': 22},
        {'month': 'February', 'total': 27},
        {'month': 'March', 'total': 23},
        {'month': 'April', 'total': 20},
        {'month': 'May', 'total': 12},
        {'month': 'June', 'total': 32},
        {'month': 'July', 'total': 42},
        {'month': 'August', 'total': 72},
        {'month': 'September', 'total': 52},
        {'month': 'October', 'total': 42},
        {'month': 'November', 'total': 92},
        {'month': 'December', 'total': 102}
    ]

    a=[]
    b=[]
    for each in data:
        x=each['month']
        y=each['total']
        a.append(x)
        b.append(y)

    
    line_chart = pygal.Line()
    line_chart.title='Total Sales in the year 2019'
    line_chart.x_labels=a
    line_chart.add('Total Sales', b)




    line_data = line_chart.render_data_uri()

    return render_template('chart.html', pie=pie_data, line=line_data)




  

    





#Run your app

if __name__== "__main__":
    app.run()
    
