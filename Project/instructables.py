from selenium import webdriver
import time
import random as rd
import sqlite3
import pandas as pd
import urllib.request as urllibX
conn = sqlite3.connect('projectables.db')
c = conn.cursor()


# def getContent():
#     '''//*[@id="intro"]/div[4]/p[1]'''
#     try:
#         p = driver.find_element_by_xpath('/html/body/main/article/div[1]/div[1]/section[1]/div[3]/p').text
#         # print(p)
#     except:
#         try:
#             p = driver.find_element_by_xpath('/html/body/main/article/div[1]/div[1]/section[1]/div[2]/p').text
#         except:
#             try:
#                 p = driver.find_element_by_xpath('//*[@id="intro"]/div[4]/p').text
#             except:
#                 p = driver.find_element_by_xpath('//*[@id="intro"]/div[2]/div/p').text
#         # print(p)

#     return p

driver = webdriver.Chrome(r"C:\Users\Utsav Singla\Downloads\Compressed\chromedriver_win32\chromedriver.exe")
driver.get("https://www.instructables.com/projects/?page=3")
time.sleep(5)
catList =[]


# /html/body/main/div/div/div[2]/div[2]/div[1]/a/img
for i in range(9,61):
    img = driver.find_element_by_xpath('//*[@id="category-projects-page"]/div/div[2]/div[2]/div[{}]/a/img'.format(i)).get_attribute('data-src')
    print(img)
    print(i)
    # //*[@id="category-projects-page"]/d>>>>>>> b2aab849f2f517fcbaedd6f20222f43e9d8e826a
# iv/div[2]/div[2]/div[8]/a/img
    # 
    # /html/body/main/div/div/div[2]/div[2]/div[12]/a/img
    # /html/body/main/div/div/div[2]/div[2]/div[12]/a/img
    # /html/body/main/div/div/div[2]/div[2]/div[11]/a/img
    savAdd = "{}.jpg".format(i)
    urllibX.urlretrieve(img, savAdd)

    # updateTable = '''UPDATE Project SET IMAGE = ? WHERE PROJECT_ID = ?;'''
    # dataInput = (savAdd,i)
    # c.execute(updateTable,dataInput)
#     driver.find_element_by_xpath('//*[@id="category-projects-page"]/div/div[2]/div[2]/div[{}]/div[1]/strong/a'.format(i)).click()
#     author = driver.find_element_by_xpath('/html/body/main/article/header/div[1]/div[1]/a[1]').text
#     category = driver.find_element_by_xpath('/html/body/main/article/header/div[1]/div[1]/a[2]').text
#     title = driver.find_element_by_xpath('/html/body/main/article/header/h1').text
#     contentBasic = getContent()
#     cost = rd.randint(500,10000)
#     rating = rd.randint(0,5)
#     ownerId = rd.randint(10000,20000)
#     categoryID = rd.randint(1000000,2000000000)
#     print(i)
#     print("author: " + author)
#     print("category: " + category)
#     print("title: " + title)
#     print("Basic content: " + contentBasic)

#     data_tuple = (i, 560+i, title,contentBasic,ownerId,cost,author,rating)
#     data_prod_Cat = (i,categoryID)
#     querySQLProduct = '''INSERT INTO Project (PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING) VALUES(?, ?, ?, ?, ?, ?, ?,?);'''
#     querySQLProd_Cat = '''INSERT INTO Categories_Project_Relation (PROJECT_ID,CATEGORY_ID) VALUES (?,?)'''


#     if category in catList:
#         queryX = '''UPDATE Categories SET NUMPROJECTS = NUMPROJECTS + 1 WHERE CATEGORY_NAME = ?; '''
#         dataX = (category,)
#     else:
#         queryX = '''INSERT INTO Categories (CATEGORY_ID,CATEGORY_NAME,NUMPROJECTS) VALUES (?,?,?)'''
#         dataX = (categoryID,category,1)
#         catList.append(category)
#     c.execute(querySQLProd_Cat, data_prod_Cat)
#     c.execute(querySQLProduct, data_tuple)
#     c.execute(queryX, dataX)

#     print(c.lastrowid)
    conn.commit()
#     driver.get("https://www.instructables.com/projects/?page=2")
    # time.sleep(5)
'''

/html/body/main/div/div/div[2]/div/div[1]/div[1]
/html/body/main/div/div/div[2]/div/div[2]/div[1]
/html/body/main/div/div/div[2]/div/div[3]/div[1]


Links of Projects
/html/body/main/div/div/div[2]/div/div[2]/div[1]/strong/a
/html/body/main/div/div/div[2]/div/div[1]/div[1]/strong/a
//*[@id="category-projects-page"]/div/div[2]/div[2]/div[1]/div[1]/strong/a
//*[@id="category-projects-page"]/div/div[2]/div[2]/div[2]/div[1]/strong/a


Author Name
/html/body/main/article/header/div[1]/div[1]/a[1]
/html/body/main/article/header/div[1]/div[1]/a[1]


Category Inside
/html/body/main/article/header/div[1]/div[1]/a[2]
/html/body/main/article/header/div[1]/div[1]/a[2]

Title
/html/body/main/article/header/h1


Step Body
/html/body/main/article/div[1]/div[1]/section[1]/div[3]/p
/html/body/main/article/div[1]/div[1]/section[1]/div[3]/p[1]
/html/body/main/article/div[1]/div[1]/section[1]/div[2]/p[1]
/html/body/main/article/div[1]/div[1]/section[1]/div[3]/p[1]
/html/body/main/article/div[1]/div[1]/section[1]/div[2]/p[1]

'''
