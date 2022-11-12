from mysql_connector import connection

# --------------------------------------------------------------
# all functions follow the same structure
# create a connection, create a query statement 
# check whether the user input is valid in terms of the
# database (i.e. if ISBN is entered exists in the specfied table in 
# the database, etc).
# If input is valid, we execute the statement using placeholders
# with string parameters that will be sent to SQL statement.
# We then return the results 
# --------------------------------------------------------------


def findAll():
    cursor = connection.cursor()
    query = "select * from bookmanager.Book"
    cursor.execute(query)
    results = cursor.fetchall()
    # connection.close()
    return results
   
def addBook(ISBN, title, year, published_by, previous_edition, price):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()

    publishercheck = "select EXISTS(SELECT name FROM Publisher WHERE name = %s)"
    precord = (published_by, )
    cursor.execute(publishercheck, precord)
    pexists = cursor.fetchall()
    if(previous_edition != None):
        prevcheck = f"select EXISTS(SELECT title FROM Book WHERE isbn = {previous_edition})"
        cursor.execute(prevcheck)
        prevexists = cursor.fetchall()
        if str(prevexists) == "[(0,)]":
            return "Book not added: specified previous edition does not exist in database. "
   #check if book with that ISBN number exists
   #this helps avoid foreign key constraint errors that stop program
    if str(result) == "[(1,)]":
        return "Book with specified ISBN already exists."
    elif str(pexists) == "[(0,)]":
        return "Speficied publisher does not exist."
    else:  
        query = """INSERT INTO Book(ISBN, title, year, published_by, previous_edition, price) VALUES (%s, %s, %s, %s, %s, %s)"""
        record = (ISBN, title, year, published_by, previous_edition, price)
        cursor.execute(query, record)
        
        connection.commit()
        # connection.close()
        result = "Added " + str(cursor.rowcount) + " book to table.\n"
        return (result)

def editISBN(current, new):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (current, )
    cursor.execute(query, record)
    result = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    else:
        query = "UPDATE Book SET ISBN = %s WHERE ISBN = %s"
        record = (new, current)
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Edited " + str(cursor.rowcount) + " ISBN.\n"
        return (result)
    
def editTitle(ISBN, title):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    else:
        query = "UPDATE Book SET title = %s WHERE ISBN = %s"
        record = (title, ISBN)
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Edited " + str(cursor.rowcount) + " title.\n"
        return (result)
    
def editPublisher(ISBN, publisher):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()

    publishercheck = "select EXISTS(SELECT name FROM Publisher WHERE name = %s)"
    precord = (publisher, )
    cursor.execute(publishercheck, precord)
    pexists = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    elif str(pexists) == "[(0,)]":
        return "Speficied publisher does not exist."
    else:
        query = "UPDATE Book SET published_by = %s WHERE ISBN = %s"
        record = (publisher, ISBN)
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Edited " + str(cursor.rowcount) + " book's publisher.\n"
        return (result)
    
def editPrice(ISBN, price):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    else:
        query = "UPDATE Book SET price = %s WHERE ISBN = %s"
        record = (price, ISBN)
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Edited " + str(cursor.rowcount) + " price.\n"
        return (result)

def editPrevEd(ISBN, prevEd):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()

    prevEdCheck = "select EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    precord = (prevEd, )
    cursor.execute(prevEdCheck, precord)
    prevExists = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    elif str(prevExists) == "[(0,)]":
        return "Speficied Previous Edition does not exist."
    else:
        query = "UPDATE CASCADE Book SET previous_edition = %s WHERE ISBN = %s"
        record = (prevEd,ISBN)
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Edited " + str(cursor.rowcount) + " previous edition.\n"
        return (result)

def deleteBook(ISBN):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT ISBN FROM Book WHERE ISBN = %s)"
    record = (ISBN, )
    cursor.execute(query, record)
    result = cursor.fetchall()
    
    if str(result) == "[(0,)]":
        return "Book with specified ISBN does not exist."
    else:
        query = "DELETE FROM Book WHERE ISBN = %s"
        record = (ISBN, )
        cursor.execute(query, record)
        connection.commit()
        # connection.close()
        result = "Deleted " + str(cursor.rowcount) + " book.\n"
        return (result)

def findByTitle(title):
    cursor = connection.cursor()
    query = f"select Exists(select ISBN from book where title like '%{title}%')"
    cursor.execute(query)
    result = cursor.fetchall()

    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select ISBN, title from Book where title like '%{title}%'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def findByISBN(ISBN):
    cursor = connection.cursor()
    query  = f"select exists(select isbn from book where isbn = {ISBN})"
    cursor.execute(query)
    result = cursor.fetchall()
    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select isbn, title from book where isbn = {ISBN}"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def findByPublisher(publisher):
    cursor = connection.cursor()
    query = f"select Exists(select ISBN from book where published_by like '%{publisher}%')"
    cursor.execute(query)
    result = cursor.fetchall()

    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select ISBN, title from Book where published_by like '%{publisher}%'"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def findByPrice(min, max):
    cursor = connection.cursor()
    query = f"select Exists(select isbn, title, price from book where price >= {min} and price <= {max})"
    cursor.execute(query)
    result = cursor.fetchall()

    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select isbn, title, price from book where price >= {min} and price <= {max}"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def findByYear(year):
    cursor = connection.cursor()
    query  = f"select exists(select isbn from book where year = {year})"
    cursor.execute(query)
    result = cursor.fetchall()
    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select isbn, title from book where year = {year}"
        cursor.execute(query)
        result = cursor.fetchall()
        return result

def findByTP(publisher, title):
    cursor = connection.cursor()
    query = f"select Exists(select ISBN from book where published_by like '%{publisher}%' and title like '%{title}%')"
    cursor.execute(query)
    result = cursor.fetchall()

    if str(result) == "[(0,)]":
        return 0
    else:
        query = f"select ISBN, title from Book where published_by like '%{publisher}%' and title like '%{title}%' "
        cursor.execute(query)
        result = cursor.fetchall()
        return result