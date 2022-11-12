# pip install mysql-connector-python
import mysql.connector


host_name = "127.0.0.1"
db_user = "root"
db_password = "password"
db_name = "bookmanager"

connection = mysql.connector.connect(host=host_name, user=db_user, 
                                    password=db_password, database=db_name) 





