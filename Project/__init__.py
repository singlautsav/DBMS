import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
import datetime

app = Flask(__name__)
UserID = 102
currentProductId = 0
def query_db(q):

   
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   # print(query)
   df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image'])
   return(df)

def query_dbX(q):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   # print(query)
   df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image','CartID','_','UserID','NUM'])
   return(df)
  
def checkLogin(user,passW):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   q = f'''SELECT * FROM Users u WHERE u.UserID = {user} and u.Password = {passW}'''
   
   try:
      c.execute(q)
      query=c.fetchall()
      # print(query)
      # print(len(query))
      return True
   except:
      return False

def getMaxBid(val = currentProductId):
   q2 = f'''SELECT MAX(BidValue) FROM Bidding WHERE ProjectID = {val};'''
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   try:
      c.execute(q2)
      query = c.fetchall()
      # print(query)
      return(query[0][0])
   except:
      return 0

def insertBid(q):
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   # print(q)
   c.execute(q)
   conn.commit()


def getallBids():
   q = f'''SELECT BidId,MAX(BidValue),UserID,ProjectID FROM Bidding GROUP BY UserID,ProjectID HAVING userid={UserID}'''
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()

   dfFinal = pd.DataFrame(columns = ['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image','maxBid'])
   try:
      abX = []
      # dfFinal = query_db(query[0][3])
      # dfFinal['maxBid'] = getMaxBid(query[0][3])
      # abX.append(dfFinal)
      for i in query:
         q=str(f'''SELECT * FROM Project WHERE (PROJECT_ID = "{i[3]}")''')
         ab = query_db(q)
         ab['maxBid'] = getMaxBid(i[3])
         ab['myBid'] = i[1]
         print(ab)
         # dfFinal.append(ab, ignore_index = True)
         abX.append(ab)
      # print(dfFinal)
      # print(ab)
      dfFinal = pd.concat(abX)
      return dfFinal
   except:
      return dfFinal

   
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
   numProject = 1
   q = f'''INSERT INTO cart (CartID,PROJECT_ID,UserID,NumProject) VALUES ({cartID},{projectID},{userID},{numProject})'''
   # vals = (cartID, projectID,userID,numProject)
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   conn.commit()
   qZ = f'''SELECT * FROM Project p, cart c WHERE p.PROJECT_ID=c.PROJECT_ID and c.UserID={userID}'''
   df = query_dbX(str(qZ))
   print(df)
   return render_template('/cart.html',data=df)


@app.route('/<idX>', methods=['GET','POST'])
def onProductClick(idX):
   print(idX)
   global currentProductId 
   currentProductId= idX
   q=str(f'''SELECT * FROM Project WHERE (PROJECT_ID = "{idX}")''')
   df=query_db(q)
   valMaxBid = getMaxBid()
   if valMaxBid ==0:
      valMaxBid = "No Bid Yet"

   df['maxBid'] = valMaxBid

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
         print("Calling Index")
         return redirect(url_for('cart'),code = 302)
      else:
         print("Calling Login")
         return redirect(url_for('login',code = 302))
   return render_template('/login.html')

@app.route('/Signup',methods = ['GET'])
def signup_page():
   return render_template('/SignUp.html')

@app.route('/SignUp/', methods = ['GET','POST'])
def add_user():
   if request.method =="POST":
      user = str(request.form['Username'])
      passW = str(request.form['Password'])
      name = str(request.form['name'])
      phoneNum = request.form['PhoneNumber']
      email = str(request.form['email'])
      print(email)
      purpose = "True"
      q = '''INSERT INTO Users (UserID,Name,PhoneNo,Email,Purpose,Password) VALUES (?,?,?,?,?,?)'''
      vals = (user,name,phoneNum,email,purpose, passW)
      conn = sqlite3.connect('projectables.db')
      c = conn.cursor()
      c.execute(q,vals)
      conn.commit()
      return redirect(url_for('login',code=302))

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
   df = getallBids()
   return render_template('/checkout.html',data = df)

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

@app.route('/bidDone/', methods = ['GET','POST'])
def checkBid():
   if request.method =="POST":
      bidValue = request.form['bidValue']
      print(bidValue)
      bidId = int(datetime.datetime.utcnow().timestamp())
      q1 = f'''INSERT INTO Bidding (BidId,BidValue,UserID,ProjectID) VALUES ({bidId},{bidValue},{UserID},{currentProductId})'''
      conn = sqlite3.connect('projectables.db')
      c = conn.cursor()
      c.execute(q1)
      conn.commit()
      # insertBid(q1)
      return redirect(url_for('onProductClick',idX=currentProductId, code=302))
   
   # return redirect(url_for('',code =302)

def getApp():
   return app

if __name__ == "__main__":
   
   app.run(debug=True)