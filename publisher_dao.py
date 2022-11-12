from mysql_connector import connection
import menu

# adds publisher to table
def addPublisher(name, phone, city):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT name FROM Publisher WHERE name = %s)"
    record = (name, )
    cursor.execute(query, record)
  
    result = cursor.fetchall()
   
    if str(result) == "[(1,)]":
        return "Publisher already exists."
        
    else: 
        query = """INSERT INTO Publisher(name, phone, city) VALUES (%s, %s, %s)"""
        record = (name, phone, city)
        cursor.execute(query, record)
    
        connection.commit()
        result = "Added " + str(cursor.rowcount) + " publisher to table.\n"
        return (result)
    

