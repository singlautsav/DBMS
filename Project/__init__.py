import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
import datetime
import os
from git import Repo

app = Flask(__name__)
UserID = 102
currentProductId = 0
currentProductUserID = "a"
currentMessageReciever = "a"

PATH_OF_GIT_REPO = os.getcwd()
COMMIT_MESSAGE = "From Script"
def git_push():
   repo = Repo(PATH_OF_GIT_REPO)
   repo.git.add(update=True)
   repo.index.commit(COMMIT_MESSAGE)
   origin = repo.remote(name='origin')
   origin.push()
   print(done)
   #  try:
        
   #  except:
   #      print('Some error occured while pushing the code')  

def hash_user(user):
   if str(user).isnumeric():
      return user
   a=0
   c=0
   for i in user:
      a+=(ord(i)-97)*(26**c)
      c+=1
   return(a)

def query_db(q):
   print(q)
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   print(query)
   global currentProductUserID
   currentProductUserID = query[0][4]
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
   q = f'''SELECT Password FROM Users u WHERE u.UserID = {str(user)}'''
   print
   # if Password == passW:
      # return
   # try:
   print(q)
   c.execute(q)
   # print(True)
   query=c.fetchall()
   print(query)
   try:
      print(query[0][0])
      if str(query[0][0])==str(passW):
         print(True)
         return True
      else:
         print(False)
         return False
   except:
      return False
   # # print(query)
   # print(len(query))
   # return True
   # except:
      # return False

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
   

   dfFinal = pd.DataFrame(columns = ['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image','maxBid'])
   try:
      q = f'''SELECT BidId,MAX(BidValue),UserID,ProjectID FROM Bidding GROUP BY UserID,ProjectID HAVING userid={UserID}'''
      conn = sqlite3.connect('projectables.db')
      c = conn.cursor()
      c.execute(q)
      query=c.fetchall()
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

def getAllUniqueMessengers(currentUserId,queryType = "sent"):
   if queryType=="sent":
      # '''SELECT DISTINCT sender FROM messages WHERE receiver = 'someuser''''
      query = f'''SELECT DISTINCT Reciever From messages WHERE Sender = {currentUserId};'''
   elif queryType=="recieved":
      query = f'''SELECT DISTINCT Sender From messages WHERE Reciever = {currentUserId};'''
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(query)
   query=c.fetchall()
   print(query)
   dfFinal = pd.DataFrame(query,columns = ['Users'])
   print(dfFinal)
   return dfFinal

def getAllMessages(SenderID,RecieverID):
   q = f'''SELECT MessageID,Reciever,Sender,MessageContent FROM messages WHERE Sender = {SenderID} and Reciever = {RecieverID}'''
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   # print(query)
   dfFinal = pd.DataFrame(query, columns = ['MessageID','Sender','Reciever','MessageContent'])
   
   q = f'''SELECT MessageID,Reciever,Sender,MessageContent FROM messages WHERE Sender = {RecieverID} and Reciever = {SenderID}'''
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()
   dfFinal2 = pd.DataFrame(query, columns = ['MessageID','Sender','Reciever','MessageContent'])
   
   # dfFinal.concat(dfFinal2,ignore_index=True)

   frames = [dfFinal,dfFinal2]
   final = pd.concat(frames,ignore_index=True)
   print(final)
   return final

# def getAllMessages(currentId,RequestedId):
#    return None


# def sendMessage(q):
   

def getallCart():
   q = f'''SELECT CartID,NumProject,UserID,Project_ID FROM cart GROUP BY UserID,Project_ID HAVING userid={UserID}'''
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   c.execute(q)
   query=c.fetchall()

   dfFinal = pd.DataFrame(columns = ['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING','Image'])
   try:
      abX = []
      # dfFinal = query_db(query[0][3])
      # dfFinal['maxBid'] = getMaxBid(query[0][3])
      # abX.append(dfFinal)
      for i in query:
         q=str(f'''SELECT * FROM Project WHERE (PROJECT_ID = "{i[3]}")''')
         ab = query_db(q)
         # ab['maxBid'] = getMaxBid(i[3])
         ab['quantity'] = i[1]
         print(ab)
         # dfFinal.append(ab, ignore_index = True)
         abX.append(ab)
      # print(dfFinal)
      # print(ab)
      dfFinal = pd.concat(abX)
      return dfFinal
   except:
      return dfFinal 

# SELECT title,category_name FROM Categories,Categories_Project_Relation,Project WHERE Categories.category_id=Categories_Project_Relation.category_id AND Project.PROJECT_ID=Categories_Project_Relation.PROJECT_ID AND Categories.CATEGORY_NAME='Cooking'
@app.route('/',methods=['GET','POST'])
def index():
   search=""
   # search=request.form['search']
   # if valX == "nothing":
   try:
      search=request.form['search']
   except:
      print("dd")
   q=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%{search}%") ORDER BY PROJECT_ID LIMIT 10''')
   df=query_db(q)
   q=str(f'''SELECT Project.PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING,Image FROM Categories,Categories_Project_Relation,Project WHERE Categories.category_id=Categories_Project_Relation.category_id AND Project.PROJECT_ID=Categories_Project_Relation.PROJECT_ID AND Categories.CATEGORY_NAME LIKE "%{search}%"''')
   df=df.append(query_db(q))
   print(df)
   # else:
      # q=str(f'''SELECT Project.PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING,Image FROM Categories,Categories_Project_Relation,Project WHERE Categories.category_id=Categories_Project_Relation.category_id AND Project.PROJECT_ID=Categories_Project_Relation.PROJECT_ID AND Categories.CATEGORY_NAME LIKE "%{valX}%"''')
      # df = que
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
   global currentProductUserID
   print(type(df['OWNER_ID']))
   print(len(df['OWNER_ID']))
   print(df['OWNER_ID'])
   # currentProductUserID = df['OWNER_ID']
   df['maxBid'] = valMaxBid
   # print(currentProductUserID)
   # print(df)
   # for i in df:
   #    print(df[i])

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
      user = hash_user(request.form['Username'])
      passW =hash_user(request.form['Password'])
      print(user,passW)
      
      if checkLogin(user,passW):
         global UserID
         UserID = user
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
      user =hash_user(str(request.form['Username']))
      passW = hash_user(str(request.form['Password']))
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

@app.route('/product_list?catx=<catX>',methods=['GET','POST'])
def product_list(catX="0"):
   print(type(catX))
   catX = int(catX)
   dictX = {1:"Cooking",2:"Circuits",3:"Workshop",4:"Craft",5:"Product"}
   category = dictX[catX]
   q=str(f'''SELECT Project.PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING,Image FROM Categories,Categories_Project_Relation,Project WHERE Categories.category_id=Categories_Project_Relation.category_id AND Project.PROJECT_ID=Categories_Project_Relation.PROJECT_ID AND Categories.CATEGORY_NAME LIKE "%{category}%"''')
   return(render_template('/product_list.html',data=query_db(q)))


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
   ins='0'
   try:
      ins = str(request.form['sel'])
      print(ins)
   except:
      # "isme jaa rha h request.form karne par :("
      print("kk")
   newest=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY PROJECT_ID LIMIT 10''')
   oldest=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY PROJECT_ID DESC LIMIT 10''')
   highest_rated=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY Rating DESC LIMIT 10''')
   lowest_rated=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY Rating LIMIT 10''')
   lowest_cost=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY COST LIMIT 10''')
   highest_cost=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%%") ORDER BY COST DESC LIMIT 10''')
   category=""
   instructions={'0':highest_cost,'1':newest,'2':oldest,'3':highest_rated,'4':lowest_rated,'5':lowest_cost,'6':highest_cost}
   filter_by_category=str(f'''SELECT Project.PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING,Image FROM Categories,Categories_Project_Relation,Project WHERE Categories.category_id=Categories_Project_Relation.category_id AND Project.PROJECT_ID=Categories_Project_Relation.PROJECT_ID AND Categories.CATEGORY_NAME LIKE "%{category}% ORDER BY [S.NO] DESC"''')
   return render_template('/Catagori.html',data=query_db(instructions[ins]))


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

@app.route('/msgDone/', methods = ['GET','POST'])
def checkMsg():
   if request.method =="POST":
      message = request.form['message']
      print(message)
      global currentProductUserID
      SenderID = str(currentProductUserID)
      msgID = int(datetime.datetime.utcnow().timestamp())
      q1 = f'''INSERT INTO messages (Sender,Reciever,MessageID,MessageContent) VALUES (?,?,?,?)'''
      vas = (UserID,SenderID,msgID,message)
      conn = sqlite3.connect('projectables.db')
      c = conn.cursor()
      c.execute(q1,vas)
      conn.commit()
      # insertBid(q1)
      return redirect(url_for('onProductClick',idX=currentProductId, code=302))


@app.route('/dashboard', methods = ['Get','POST'])
def Dashboard():
   df = getallBids()
   df2 = getallCart()
   dfRecieved =getAllUniqueMessengers(UserID,"recieved")
   dfSent = getAllUniqueMessengers(UserID,"sent")
   content = {"bids": df, "carts": df2, "messagesRecieved":dfRecieved, "messagesSent":dfSent}

   return render_template('/Dashboard.html',data = content)
  
@app.route('/messages?idX=<idX>', methods = ['GET','POST'])

def Messages(idX):
   df = getAllMessages(UserID,idX)
   global currentMessageReciever
   currentMessageReciever = idX
   return render_template('/Messages.html', data = df)

@app.route('/messageSent/', methods=['GET','POST'])
def messageSent():
   if request.method =="POST":
      message = request.form['message']
      print(message)
      # global currentProductUserID
      SenderID = str(currentMessageReciever)
      msgID = int(datetime.datetime.utcnow().timestamp())
      q1 = f'''INSERT INTO messages (Sender,Reciever,MessageID,MessageContent) VALUES (?,?,?,?)'''
      vas = (UserID,SenderID,msgID,message)
      conn = sqlite3.connect('projectables.db')
      c = conn.cursor()
      c.execute(q1,vas)
      conn.commit()
      # insertBid(q1)
      return redirect(url_for('Dashboard', code=302))

def getApp():
   return app

if __name__ == "__main__":
   git_push()
   # app.run(debug=True)
