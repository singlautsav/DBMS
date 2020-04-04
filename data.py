import sqlite3
import pandas as pd
conn = sqlite3.connect('projectables.db')  
c = conn.cursor()
c.execute('''SELECT * FROM Project''')
query=c.fetchall()
print(query)
df = pd.DataFrame(query,columns=['PROJECT_ID','[S.NO.]','TITLE','CONTENT','OWNER_ID','COST','AUTHOR','RATING'])
print(df)