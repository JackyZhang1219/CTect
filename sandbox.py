import mysql.connector

dbConn = mysql.connector.connect(
    user='admin',
    password='pdfstoragedatabase',
    host='pdfstore-database.c5ggmgyguhw5.us-east-2.rds.amazonaws.com',
    database='sys'
)

dbCursor = dbConn.cursor()
dbCursor.execute("SHOW DATABASES")

for dbname in dbCursor:
    print(dbname)

dbCursor.close()
dbConn.close()
