import sqlite3
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for,Markup,request
conn = sqlite3.connect('projectables.db')  
c = conn.cursor()
c.execute('''SELECT * FROM Project''')
query=c.fetchall()
df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING'])
print(df)
app = Flask(__name__)
# app._static_folder = "/static"
@app.route('/',methods=['GET'])
def index():
   return(render_template('/product_list.html'))
if __name__ == "__main__":
   app.run(debug=True)