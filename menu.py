import sys
import book_dao
import publisher_dao


# --------------------------------------------------------------
# This program creates a user interface to manage an SQL Database
# that contains books and publishers. Allows the user to add a publisher/book
# remove books, edit books and their attributes, search for books
# given certain criteria.


# all functions follow similar structure:
# print user instructions and then get user input
# after getting the attributes needed, check whether
# input is valid (i.e. if isbn is 10 digits and only numbers),
#  functions then call the functions in book_dao file where 
# we start the connection and execute the SQL commands 
# in the required format.
# --------------------------------------------------------------

# ****************************
#       DICT FOR MENUS
# ****************************
# options for main menu
menu_options = {
    1: 'Add a Publisher',
    2: 'Add a Book',
    3: 'Edit a Book',
    4: 'Delete a Book',
    5: 'Search Books',
    6: 'Exit',
}

# options for search menu
search_menu_options = {
    1: 'All Books',
    2: 'Title',
    3: 'ISBN',
    4: 'Publisher',
    5: 'Price range',
    6: 'Year',
    7: 'Title and Publisher',
}

# optinos for edit book menu
editBook_menu_options = {
    1: 'ISBN',
    2: 'Title',
    3: 'Year',
    4: 'Publisher',
    5: 'Previous Edition',
    6: 'Price',
}

# ****************************
#       SEARCH OPTIONS
# ****************************
# returns all books
def search_all_books():
    # Use a data access object (DAO) to 
    # abstract the retrieval of data from 
    # a data resource such as a database.
    results = book_dao.findAll()
    # Display results
    print("The following are the ISBNs and title of all books.")
    for item in results:
        print(item[0], item[1])
    print("The end of books.")

# finds book by specified title
def search_by_title():
    title = str(input("Enter Book Title: "))
    res = book_dao.findByTitle(title)
    if res == 0:
        print("No books matched your search.")
    else:
        print("The following are the ISBNs and titles of books that matched your search.")
        for item in res:
            print(item[0], item[1])
        print("The end of books.")

# finds book by specified isbn
def search_by_ISBN():
    # get isbn from user. isbn has to be 10 chars long and only numbers
    try:
        ISBN = str(input("Enter book ISBN: "))
        assert len(ISBN) == 10 and ISBN.isdigit(), print("\nInvalid ISBN enetered.\n") 
    except AssertionError as msg:
            print("Try again...\n")

    res = book_dao.findByISBN(ISBN)
    if(res == 0):
        print("\nNo book matched your search.")
    else:
        print("The following book matched your search:")
        for book in res:
            print(book[0], book[1])

# finds book by specified publisher
def search_by_publisher():
    publisher = str(input("Enter Publisher: "))
    res = book_dao.findByPublisher(publisher)
    if res == 0:
        print("No books matched your search.")
    else:
        print("The following are the ISBNs and titles of books from specified Publisher.")
        for item in res:
            print(item[0], item[1])
        print("The end of books.")

# finds book by specified price range
def search_by_price():
    min = str(input("Enter minimum price: "))
    max = str(input("Enter maximum price: "))
    
    res = book_dao.findByPrice(min, max)
    if res == 0:
        print("No books matched your search.")
    else:
        print("The following are the ISBNs, titles, and prices of books from specified price range.")
        print("ISBN      ", "Title                ", "Price")
        for item in res:
            print(item[0], item[1], item[2])
        print("The end of books.")
    
# finds book by specified year
def search_by_year():
   # get year from user.
    try:
        year = str(input("Enter Year: "))
        assert len(year) == 4 and year.isdigit(), print("\nInvalid year enetered.\n") 
    except AssertionError as msg:
            print("Try again...\n")

    res = book_dao.findByYear(year)
    if(res == 0):
        print("\nNo book matched your search.")
    else:
        print("The following book matched your search:")
        for book in res:
            print(book[0], book[1])

# finds book by specified title and publisher
def search_by_TP():
    title = str(input("Enter Title: "))
    publisher = str(input("Enter Publisher: "))
    res = book_dao.findByTP(publisher, title)
    if res == 0:
        print("No books matched your search.")
    else:
        print("The following are the ISBNs and titles of books from specified Title and Publisher.")
        for item in res:
            print(item[0], item[1])
        print("The end of books.")


def print_menu():
    print()
    print("Please make a selection")
    for key in menu_options.keys():
        print (str(key)+'.', menu_options[key], end = "  ")
    print()
    print("The end of top-level options")
    print()


# ****************************
#       main menu options
# ****************************
# option 1 allows user to add a publisher
def option1():
    while(True):
        # get input from user: publisher has name, phone and city
        try:
            print()
            name = str(input("Enter publisher name: "))
            assert len(name) <= 25, print("Publisher name cannot contain more than 25 characters\n") 

            phone = str(input("Enter publisher phone number: "))
            assert len(phone) == 10, print("\nInvalid phone number.\n") 

            city = str(input("Enter publisher city: "))
            assert len(city) <= 20, print("City cannot contain more than 20 characters\n") 
    # check if attritube constraints are met
        except AssertionError as msg:
            print("Try again...\n")
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        else:
            break
    # calls addPublisher function
    res = publisher_dao.addPublisher(name, phone, city)
    print()
    print(res)
    
#option 2 allows user to add a book
def option2():
    while(True):
        # get input from user
        try:
            print()
            ISBN = str(input("Enter ISBN: "))
            assert len(ISBN) == 10, print("ISBN must contain 10 characters\n") 

            title = str(input("Enter book title: "))
            assert len(title) < 50, print("\nTitle is too long.\n") 

            year = int(input("Enter year: "))
            assert 1900 <= year <= 2022, print("Invalid year.\n") 

            published_by = str(input("Publisher: "))
            previous_edition = str(input("Previous edition ISBN (Or enter 'None'): "))
            if previous_edition == "None":
                previous_edition = None
            price = float(input("Price: "))

    # check if attritube constraints are met
        except AssertionError as msg:
            print("Try again...\n")
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        else:
            break
    # calls addBook function
    res = book_dao.addBook(ISBN, title, year, published_by, previous_edition, price)
    print()
    print(res)

#option 3 allows user to edit an existing book
def option3():
    # while(True):
    while(True):
        print()
        print("Select an attribute to edit: ")
        for key in editBook_menu_options.keys():
            print(str(key)+'.', editBook_menu_options[key], end = " ")
        print()
        
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
            current = str(input("Enter current ISBN: "))
            new = str(input("Enter new ISBN: "))
            res = book_dao.editISBN(current, new)
            print()
            print(res)
            
        elif option == 2:
            ISBN = str(input("Enter book ISBN: "))
            title = str(input("Enter new Title: "))
            res = book_dao.editTitle(ISBN, title)
            print()
            print(res)
        elif option == 3:
            ISBN = str(input("Enter book ISBN: "))
            year = int(input("Enter new year: "))
            res = book_dao.editYear(ISBN, year)
            print()
            print(res)
        elif option == 4:
            ISBN = str(input("Enter book ISBN: "))
            publisher = str(input("Enter new publisher: "))
            res = book_dao.editPublisher(ISBN, publisher)
            print()
            print(res)
        # option 5 won't work because previous_edition is a child 
        # row so we cannot update the previous edition because of 
        # foreign key constraints
        elif option == 5:
            ISBN = str(input("Enter current ISBN: "))
            prevEd = str(input("Enter new Previous Edition ISBN: "))
            res = book_dao.editISBN(ISBN, prevEd)
            print()
            print(res)
        elif option == 6:
            ISBN = str(input("Enter book ISBN: "))
            price = str(input("Enter new price: "))
            res = book_dao.editPrevEd(ISBN, price)
            print()
            print(res)
        else:
            print('Invalid option. Please enter a number between 1 and 6.')
        break

# delete a book
def option4():
    while(True):
        # get input from user
        try:
            print()
            ISBN = str(input("Enter ISBN: "))
            assert len(ISBN) == 10, print("ISBN must contain 10 characters\n") 
    # check if attritube constraints are met
        except AssertionError as msg:
            print("Try again...\n")
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        else:
            break
    # calls addBook function
    res = book_dao.deleteBook(ISBN)
    print()
    print(res)

# seaerch a book
def option5():
    # A sub-menu is printed
    # and prompt user selection
    while(True):
        print()
        print("Select an attribute to search by: ")
        for key in search_menu_options.keys():
            print(str(key)+'.', search_menu_options[key], end = "  ")
        print()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            print('Wrong input. Please enter a number ...')

    # user selection of options and actions
        if option == 1:
            print("Search Option 1: all books were chosen.")
            search_all_books()
        elif option == 2:
            print("Search Option 2: Find by title was chosen.")
            search_by_title()
        elif option == 3:
            print("Search option 3: Find by ISBN")
            search_by_ISBN()
        elif option == 4:
            print("Search option 4: Find by Publisher")
            search_by_publisher()
        elif option == 5:
            print("Search option 5: Find by price range")
            search_by_price()
        elif option == 6:
            print("Search option 6: Find by year")
            search_by_year()
        elif option == 7:
            print("Search option 7: Find by title and publisher")
            search_by_TP()
        break

if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            print('Thanks your for using our database services! Bye')
            book_dao.connection.close()
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')











