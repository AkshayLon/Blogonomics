import mysql.connector

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

class mysqlTable():
  def __init__(self, name):
    self.name = name
    columns = MySQLexecute('SHOW COLUMNS FROM sql2383197.' + name + ";")
    self.columns = list()
    for column in columns :
      self.columns.append(column[0])
    tempColumns = self.columns
    tempColumns.pop(0)
    self.columnsUse = str(tuple(tempColumns)).replace("'", "")

  def addRow(self, row):
    MySQLexecute("INSERT INTO sql2383197." + self.name + " " + self.columnsUse + " VALUES " + str(tuple(row)) + ";", False)

  def updateValue(self, columnToUpdate, setValue, idSearch):
    MySQLexecute("UPDATE sql2383197." + self.name + " SET " + columnToUpdate + " = '" + setValue + "' WHERE id = '" + str(idSearch) + "';", False)

  def getValue(self, columnWanted, id):
    value = MySQLexecute("SELECT " + columnWanted + " FROM sql2383197." + self.name + " WHERE id=" + str(id) + ";")
    value = value[0][0]
    return value

  def deleteRow(self, id):
    MySQLexecute("DELETE FROM sql2383197." + self.name + " WHERE id=" + str(id) + ";", False)

  def checkExists(self, tupleRow):
    all = MySQLexecute("SELECT * FROM sql2383197." + self.name + ";")
    if tupleRow in all:
      return True
    return False
