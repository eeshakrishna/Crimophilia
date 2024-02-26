import mysql.connector
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Tweety2002**',
    port='3306'
)


my_cursor=mydb.cursor()
my_cursor.execute("CREATE DATABASE DBMSP")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

