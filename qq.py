import mysql.connector

connection = mysql.connector.connect(host='localhost',
                                         database='bookb123',
                                         user='root',
                                         password='Tweety2002**')

"""
    sql_select_Query = "select * from User"
    sql_select_Query1 = "select username from User"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query1)
    records = cursor.fetchall()
    print("Total number of rows in table: ", cursor.rowcount)
    
    print("\nPrinting each row")
    for row in records:
        print("Fname = ", row[0], )
        #print("LName = ", row[1])
        #print("Email  = ", row[2])
        #print("Age  = ", row[3], "\n")
"""