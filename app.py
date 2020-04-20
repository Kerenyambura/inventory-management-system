#Importing
#import filename
#from filename import.....

from flask import Flask,render_template,request,redirect,url_for

import pygal

import psycopg2

from flask_sqlalchemy import SQLAlchemy

from config.config import Development,Production



''' 
    We have two ways for connecting to the database in flask
    1. psycopg2 - Here you write SQL statements
    2. Flask-SQLAlchemy - Here you use ORM(Object Relational Mapper)

    PSYCOPG2
    Its a python library that helps write queries in flask
    HOW TO USE IT
    1. install it

    2. set up a connection to your database 
        - username
        - password
        - port
        - root
        - dbname

    3. connect to using cursor
    4. execute an SQL Statement
    5. Fetch your records
'''


'''
    FLASK-SQLALCHEMY
    Library that helps us write classes object to communicate to our database without
    writing sql statements

    EXAMPLE 
    INSERT INTO sales VALUES (inv_id=1, quantity=10, created=now())

    create a class and it SalesModel
    then create function that inserts records
    then insert

    class SalesModel():
        def insert_sales(self):
            db.session.add()
        
    query

        def query_sales(self):
            self.query.all()

        select * from sales


    STEPS TO USE FLASK-SQLALCHEMY
    1. install it
    2. use it
        - create a connection to the db
        - load configurations
        - create an instance of FLASK-SQLALCHEMY by passing in the app


'''

# calling/ instanciating
app = Flask(__name__)

# Load configuration
app.config.from_object(Development)

# calling/ instanciating of SQLAlchemy
# alway comes with functions and helpers to create our tables
db = SQLAlchemy(app)

# Creating of endpoints/ routes
# 1. declaration of a route
# 2. a function embedded to the route
conn = psycopg2.connect(" dbname='inventory_management_system' user='postgres' host='localhost' port='5432' password='Goodmand254' ")
cur = conn.cursor()

# creating tables
from models.Inventory import InventoryModel
from models.Sales import SalesModel
from models.Stock import StocksModel


@app.before_first_request
def create_tables():
    db.create_all()  


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
    inventories= InventoryModel.fetch_all_inventories()
    inventories=InventoryModel.query.all()
    

    cur.execute("""


    SELECT invid, sum(quantity) as "remaining_stock"
		FROM (SELECT st.invid, sum(stock) as "quantity"
		FROM public.new_stocks as st
		GROUP BY invid
			
			union all
			 
	SELECT sa.invid, - sum(quantity) as "quantity"
		FROM public.new_sales as sa
		GROUP BY invid) as stsa
		GROUP BY invid
		ORDER BY invid;

    """)

    rs = cur.fetchall()
    
    #receive from a form

    if request.method == 'POST':
        name=request.form['name']
        inv_type=request.form['type']
        buying_price=request.form['buying_price']
        selling_price=request.form['selling_price']
        
        new_inv=InventoryModel(name=name,inv_type=inv_type,buying_price=buying_price,selling_price=selling_price)
        new_inv.add_inventories()

        return redirect( url_for ('inventories'))


        
    return render_template('inventories.html', inventories=inventories, remaining_stock=rs)


@app.route('/add_stock/<invid>', methods=['POST'])
def add_stock(invid):
    if request.method=='POST':
         stock = request.form['stock']
          
         new_stock = StocksModel(invid=invid,  stock=stock)
         new_stock.add_stock()
         #remstock=new_stock-new_sale

    

    #print(quantity)
    return redirect( url_for ('inventories'))


@app.route('/add_sale/<invid>', methods=['POST'])
def add_sale(invid):
    if request.method == 'POST':
        sale = request.form['quantity']
        new_sale=SalesModel(invid=invid, quantity=sale)

        new_sale.add_sales()
    #print(quantity)
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

@app.route('/edit', methods=['GET', 'POST'])
def edit():

    # recieve from a form
    
    if request.method == 'POST':
        name = request.form['name']
        inv_type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        print(name)
        print(inv_type)
        print(buying_price)
        print(selling_price)

        return redirect(url_for('inventories'))
 
    
@app.route('/data_visualisation')
def data_visualisation():

    conn = psycopg2.connect(" dbname='inventory_management_system' user='postgres' host='localhost' port='5432' password='Goodmand254' ")
    
    cur = conn.cursor()
    cur.execute("""
    SELECT type, count(type) 
    FROM public.inventories
    group by type;
    """)

    product_service = cur.fetchall()
    print(product_service)


    pie_chart = pygal.Pie()

    '''my_pie_data = [
        ('Nairobi', 63),
        ('Mombasa', 20),
        ('Kilifi', 17),
        ('Machakos', 30),
        ('Kiambu', 7)]'''

    pie_chart.title='Ratio of product and service'
    for each in product_service:
        pie_chart.add(each[0],each[1])

   
    
    pie_data = pie_chart.render_data_uri()




    #end of pie chart

    #start of line graph



    cur.execute("""
    select to_char(to_timestamp (EXTRACT(MONTH FROM  s.created_at)::text, 'MM'), 'Mon') as Month,sum(quantity*selling_price) as total_sales
    from sales as s
    join inventories as i on s.invid = i.id
	group by month
	order by month;
    """)

    monthly_sales=cur.fetchall()
    print(monthly_sales)
  

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
    for each in monthly_sales:
   
        a.append(each[0])
        b.append(each[1])

    
    line_chart = pygal.Line()
    line_chart.title='Total Sales in the year 2019'
    line_chart.x_labels=a
    line_chart.add('Total Sales', b)




    line_data = line_chart.render_data_uri()

    return render_template('chart.html', pie=pie_data, line=line_data)

@app.route('/view_sales/<invid>')
def view_sales(invid):

    sales = SalesModel.get_sales_by_id(invid)
    inv_name = InventoryModel.fetch_by_id(invid)

    return render_template('viewSales.html', sales=sales,inv_name=inv_name)





  

    





#Run your app

if __name__== "__main__":
    app.run()
    
