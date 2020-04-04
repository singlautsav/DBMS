from selenium import webdriver
import time
import random as rd
import sqlite3
import pandas as pd

conn = sqlite3.connect('projectables.db')
c = conn.cursor()


def getContent():
    try:
        p = driver.find_element_by_xpath('/html/body/main/article/div[1]/div[1]/section[1]/div[3]/p').text
        # print(p)
    except:
        p = driver.find_element_by_xpath('/html/body/main/article/div[1]/div[1]/section[1]/div[2]/p').text
        # print(p)

    return p

driver = webdriver.Chrome(r"C:\Users\Utsav Singla\Downloads\Compressed\chromedriver_win32\chromedriver.exe")
driver.get("https://www.instructables.com/projects/")
time.sleep(5)
for i in range(1,61):
    driver.find_element_by_xpath('//*[@id="category-projects-page"]/div/div[2]/div[2]/div[{}]/div[1]/strong/a'.format(i)).click()
    author = driver.find_element_by_xpath('/html/body/main/article/header/div[1]/div[1]/a[1]').text
    category = driver.find_element_by_xpath('/html/body/main/article/header/div[1]/div[1]/a[2]').text
    title = driver.find_element_by_xpath('/html/body/main/article/header/h1').text
    contentBasic = getContent()
    cost = rd.randint(500,10000)
    rating = rd.randint(0,6)
    print(i)
    print("author: " + author)
    print("category: " + category)
    print("title: " + title)
    print("Basic content: " + contentBasic)
    data_tuple = (i, 500+i, title,contentBasic,cost,author,rating)
    querySQL = '''INSERT INTO Project (PROJECT_ID,[S.NO.],TITLE,CONTENT,OWNER_ID,COST,AUTHOR,RATING) VALUES(?, ?, ?, ?, ?, ?, ?);'''
    c.execute(querySQL,data_tuple)
    print(c.lastrowid)
    conn.commit()
    driver.get("https://www.instructables.com/projects/")
    time.sleep(5)
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