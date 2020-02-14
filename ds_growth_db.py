import mysql.connector

# MySQL DB connector
mydb = mysql.connector.connect(
        host="localhost",
        user="your_username",
        passwd="your_password",
        database="database_name")
mycursor = mydb.cursor()


# To create database and tables
def create_database():
    mycursor.execute("CREATE DATABASE database_name")
    mycursor.execute("CREATE TABLE table_name (designation VARCHAR(255), company VARCHAR(255), skill VARCHAR(300), salary VARCHAR(255), posted_on VARCHAR(255), location VARCHAR(255), min_experience VARCHAR(255),max_experience VARCHAR(255))")
    # To view the created tables
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
      print(x)

def insert_data(extracted_data):
    sql = """INSERT INTO table_name (designation, company, skill, salary, posted_on, location, min_experience, max_experience) VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)"""
    mycursor.executemany(sql, extracted_data)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")

# To check the loaded data 
def check():
    mycursor.execute("SELECT * FROM table_name")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


# Call these functions only if it is needed
# create_database()
# insert_data()
# check()