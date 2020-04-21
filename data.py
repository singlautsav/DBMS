import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
import datetime

app = Flask(__name__)
UserID = 102
def query_db(q):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   print(query)
   df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image'])
   return(df)

def query_dbX(q):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   print(query)
   df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image','CartID','_','UserID','NUM'])
   return(df)
  
def checkLogin(user,passW):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   q = f'''SELECT * FROM Users u WHERE u.UserID = {user} and u.Password = {passW}'''
   
   try:
      c.execute(q)
      query=c.fetchall()
      print(query)
      print(len(query))
      return True
   except:
      return False
   # df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image','CartID','_','UserID','NUM'])
   # return(df)

# @app.route('/product_list',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
   search=""
   try:
      search=request.form['search']
   except:
      print("dd")
   q=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%{search}%") ORDER BY PROJECT_ID LIMIT 10''')
   df=query_db(q)
   print(df)
   return(render_template('/product_list.html',data=df))

@app.route('/cart', methods=['GET'])
def addToCart():
   # print()
   check = request.args.get('idX', '')
   print(check)
   cartID = int(datetime.datetime.utcnow().timestamp())
   projectID = check
   userID = UserID
   numProject = l
   q = f'''INSERT INTO cart (CartID,PROJECT_ID,UserID,NumProject) VALUES ({cartID},{projectID},{userID},{numProject})'''
   # vals = (cartID, projectID,userID,numProject)
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   conn.commit()

   # qX = f'''SELECT * FROM Project WHERE PROJECT_ID = (SELECT PROJECT_ID,* FROM cart WHERE(UserID={userID})))'''
   qZ = f'''SELECT * FROM Project p, cart c WHERE p.PROJECT_ID=c.PROJECT_ID and c.UserID={userID}'''
   # conn = sqlite3.connect('projectables.db')
   # c = conn.cursor()
   # c.execute(q)
   # query=c.fetchall()
   # print(query)
   # )
   df = query_dbX(str(qZ))
   print(df)

   #  product = Product.query.filter(Product.id == product_id)
   #  cart_item = CartItem(product=product)
   #  db.session.add(cart_item)
   #  db.session.commit()

   # return render_template('index.html')
   return render_template('/cart.html',data=df)


@app.route('/<idX>', methods=['GET','POST'])
def onProductClick(idX):
   print(idX)
   q=str(f'''SELECT * FROM Project WHERE (TITLE = "{idX}")''')
   df=query_db(q)
   print(df)
   for i in df:
      print(df[i])

   return (render_template('/single-product.html',data=df))

@app.route('/index',methods = ['GET','POST'])
def index_page():
   return (render_template('/index.html'))


@app.route('/login', methods = ['GET','POST'])
def login():
   return render_template('/login.html')

@app.route('/CheckingLogin/', methods = ['GET','POST'])
def login_page():
   if request.method == "POST":
      user = request.form['Username']
      passW = request.form['Password']
      print(user,passW)
      global UserID
      UserID = user
      if checkLogin(UserID,passW):
         return redirect(url_for('index'),code = 302)
      else:
         return redirect(url_for('login',code = 302))
   return render_template('/login.html')

@app.route('/product_list',methods=['GET','POST'])
def product_list():
   search=""
   try:
      search=request.form['search']
   except:
      print("dd")
   q=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%{search}%") ORDER BY [S.NO.] DESC LIMIT 10''')
   df=query_db(q)
   print(df)
   print(search)
   return(render_template('/product_list.html',data=df))


@app.route('/myCart',methods=['GET','POST'])
def cart():
   userID = UserID
   qZ = f'''SELECT * FROM Project p, cart c WHERE p.PROJECT_ID=c.PROJECT_ID and c.UserID={userID}'''
   df = query_dbX(str(qZ))
   print(df)
   return render_template('/cart.html',data=df)


@app.route('/checkout', methods = ['Get','POST'])
def checkout():
   return render_template('/checkout.html')

@app.route('/about', methods = ['Get','POST'])
def about():
   return render_template('/about.html')

@app.route('/blog', methods = ['Get','POST'])
def blog():
   return render_template('/blog.html')


@app.route('/Catagori', methods = ['Get','POST'])
def Catagori():
   return render_template('/Catagori.html')


@app.route('/Confirmation', methods = ['Get','POST'])
def Confirmation():
   return render_template('/confirmation.html')


@app.route('/contact', methods = ['Get','POST'])
def contact():
   return render_template('/contact.html')

@app.route('/elements', methods = ['Get','POST'])
def elements():
   return render_template('/elements.html')

@app.route('/main', methods = ['Get','POST'])
def main():
   return render_template('/main.html')

@app.route('/single-blog', methods = ['Get','POST'])
def single_blog():
   return render_template('/single-blog.html')





if __name__ == "__main__":
   
   app.run(debug=True)