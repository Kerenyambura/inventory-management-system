#Importing
#import filename
#from filename import.....

from flask import Flask,render_template,request,redirect,url_for

import pygal

import psycopg2



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
    SELECT EXTRACT(MONTH FROM s.created_at) as sales_month, sum(quantity*selling_price) as total_sales
    from sales as s
    join inventories as i on s.invid = i.id
	group by sales_month 
	order by sales_month asc;
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




  

    





#Run your app

if __name__== "__main__":
    app.run()
    
