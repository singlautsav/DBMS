import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request


app = Flask(__name__)
  

@app.route('/',methods=['GET','POST'])
def index():
   search=""
   try:
      search=request.form['search']
   except:
      print("dd")
   conn = sqlite3.connect('projectables.db')
   c = conn.cursor()
   q=str(f'''SELECT * FROM Project WHERE (TITLE LIKE "%{search}%") ORDER BY [S.NO.] DESC LIMIT 10''')
   c.execute(q)
   query=c.fetchall()
   df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING'])
   print(df)
   print(search)
   return(render_template('/product_list.html',data=df))

@app.route('/<idX>', methods=['GET','POST'])
def onProductClick(idX):
   print(idX)
   return (render_template('/single-product.html'))

@app.route('/index',methods = ['GET','POST'])
def index_page():
   return (render_template('/index.html'))


@app.route('/login', methods = ['GET','POST'])
def login():
   return render_template('/login.html')


@app.route('/product_list',methods=['GET','POST'])
def product_list():
   return render_template('/product_list.html')


@app.route('/myCart',methods=['GET','POST'])
def cart():
   return render_template('/cart.html')


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