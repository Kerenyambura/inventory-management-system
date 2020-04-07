#Importing
#import filename
#from filename import.....

from flask import Flask,render_template,request,redirect,url_for

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








#Run your app

if __name__== "__main__":
    app.run()
    
