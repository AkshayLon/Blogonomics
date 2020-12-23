from flask import Flask, redirect, render_template, url_for, request
from TableClass import mysqlTable
import mysql.connector
import datetime

def MySQLexecute(SQL_String, results=True):
  databaseConnect = mysql.connector.connect(
    port="3306",
    host="sql2.freesqldatabase.com",
    user="sql2383197",
    password="SchoolStuff@2020",
    database="sql2383197",
    autocommit=True
  )
  cursor = databaseConnect.cursor()
  cursor.execute(SQL_String)
  if results:
    output = cursor.fetchall()

  databaseConnect.commit()
  cursor.close()
  databaseConnect.close()
  if results:
    return output

blogTable = mysqlTable('blogs')
accessTable = mysqlTable('access')
authorsTable = mysqlTable('authors')

def getHomeBlogs():
    nonArchived = MySQLexecute('SELECT * FROM sql2383197.blogs WHERE Archived=0;')
    lastWeek = datetime.date.today() - datetime.timedelta(days=7)
    counts = list()
    for blog in nonArchived:
        count = MySQLexecute("SELECT COUNT(BlogId) FROM sql2383197.access WHERE BlogId='" + str(blog[0]) + "' AND DateAccessed > '" + str(lastWeek) + "';")
        counts.append(count[0][0])
    maxBlog = counts.index(max(counts))
    nonArchived.append(nonArchived.pop(maxBlog))
    return nonArchived

def authors():
    authors = list()
    for blog in getHomeBlogs():
        names = MySQLexecute('SELECT Name, Surname FROM sql2383197.authors where id=' + str(blog[2]))
        authors.append(names[0][0] + " " + names[0][1])
    return authors

app = Flask(__name__)

@app.route('/Home', methods=['GET', 'POST'])
def home():
    return render_template('main.html', blogs=getHomeBlogs(), authors=authors())

@app.route('/Archive', methods=['GET', 'POST'])
def archive():
    return render_template('archive.html')

@app.route('/Blog/<Blog>', methods=['GET', 'POST'])
def blog(Blog):
    BlogId = MySQLexecute("SELECT id FROM sql2383197.blogs WHERE File='" + Blog + "';")
    accessTable.addRow([BlogId[0][0], str(datetime.date.today())])
    return render_template(Blog)

if __name__ == '__main__':
    app.run(debug=True)