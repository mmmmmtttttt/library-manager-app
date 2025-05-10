"""
Library Management Program
This program manages the entire library by:
1- Viewing all books
2- Adding a library
3- Editing
4- Deleting
5- Borrowing a book
6- Returning a book
7- Viewing borrowed books
8- Searching for a book by name
9- Sign_out
"""

import sqlite3

class Library:
    def __init__(self):
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect("D:\GitHub\library-manager-app\Library.db")
            self.cursor = self.conn.cursor()
            # Create the books and users and borrowed_books tables if they don't exists
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    borrowed INTEGER DEFAULT 1
                )
            ''')
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    password TEXT
                )
            ''')
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS borrowed_books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    book_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (book_id) REFERENCES books (id)
                )
            ''')
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
        finally:
            # Commit the changes done to the database
            self.conn.commit()

    def sign_choices(self):
        print('''
                Welcome to the Library Management System
            
                    1. Sign Up
                    2. Sign In
                    3. Exit
            ''')
        self.choice = int(input("Enter your choice (1-3): ").strip())
        if self.choice == 1:
            self.sign_up()
        elif self.choice == 2:
            self.sign_in()
        elif self.choice == 3:
            self.quit()
            return
        else:
            print("Choice is not found, please choice round (1-3)")
        
    def quit(self):
        self.conn.commit()
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("save and closed done!")
        print("Exit the library...")

    def sign_up(self):
        print("""
                        Create a new account
            """)
        self.name = input("Enter your name: ").strip().capitalize()
        self.email = input("Enter your email: ").strip()
        self.password = input("Create a password: ").strip()
        self.cursor.execute("SELECT name FROM users")
        self.user = self.cursor.fetchone()
        if self.name == self.user:
            print("This user already exists")
            return
        self.cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (self.name, self.email, self.password))
        print(f"Create User: {self.name} Successfully")
        self.conn.commit()
        print("You can log in to the library.")
        self.sing_in()

    def sign_in(self):
        self.count = 3
        while self.count > 0:
            print("""
                            Library login
                """)
            self.name = input("Enter Your UserName: ").strip().capitalize()
            self.password = input("Enter Your Passsword: ").strip()
            self.cursor.execute("SELECT name, password FROM users WHERE name = ? AND password = ? ", (self.name, self.password))
            self.check = self.cursor.fetchone()
            if self.check:
                self.run()
            else:
                self.count -= 1
                print("Incorrect username or password. Please try again.")
                print(f"Number of remaining attempts: {self.count}")
        else:
            print("You have filled in the available attempts.\nPlease create an account if you don't have one.")
            print('''
                            1- Forget Password
                            2- Create new acount
                ''')
            self.choice = int(input("Enter yuor choice: ").strip())
            if self.choice == 1:
                self.forget_password()
            elif self.choice == 2:
                self.sign_up()

    def forget_password(self):
        print("""
                        Return your acount
            """)
        self.cursor.execute("SELECT name, password FROM users")
        self.users = self.cursor.fetchall()
        # print(self.users)
        self.name = input("Enter your name: ").strip().capitalize()
        for self.user in self.users:
            # print(self.user[0])
            if self.name == self.user[0]:
                print(f"Username: {self.user[0]}")
                print(f"Password: {self.user[1]}")
                self.sign_in()
        else:
            print("No acount this name")
            self.sign_choices()

    def view_All_Books(self):
        print("""
                        Views All Books in Library
            """)
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        if not self.books:
            print("This Library is 'Empty'")
            return
        for i, self.book in enumerate(self.books, start=1):
            print(f"{i}- ID: {self.book[0]} - Title: {self.book[1]} - Author: {self.book[2]} - Year: {self.book[3]}")

    def show_choices(self):
        print('''
                Welcome to the Library Management System
            
                        1. View all books
                        2. Add a book
                        3. Edit a book
                        4. Delete a book
                        5. Borrowing a book
                        6. Return a book
                        7. View borrowed books
                        8. Search for a book by name
                        9. Sign Out
            ''')
        self.choice = int(input("Enter the number of the operation you want to perform (1-9): "))

    def add_book(self):
        print("""
                        Add Book in Library
            """)
        self.title = input("Enter Title the book: ").strip()
        self.author = input("Enter Author the book: ").strip().capitalize()
        self.year = int(input("Enter Year the book: ").strip())
        self.borrowed = bool(input("Enter Borrowed the book (True/False)").strip().capitalize())
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        for self.book in self.books:
            if self.title == self.book[1] and self.author == self.book[2] and self.year == self.book[3]:
                print("This book already in the library")
        self.cursor.execute("INSERT INTO books (title, author, year, borrowed) VALUES (?, ?, ?, ?)", 
                            (self.title, self.author, self.year, self.borrowed))
        self.conn.commit()
        print(f"This book: '{self.title}' is added successfully")
        
    def edit_book(self):
        print("""
                        Edit book
            """)
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        if not self.books:
            print("No books in library")
            return
        self.view_All_Books()
        self.id = int(input("Enter ID book for edit: "))
        print("""
                        You can edit
            """)
        self.title = input("Enter Title the book: ").strip()
        self.author = input("Enter Author the book: ").strip().capitalize()
        self.year = int(input("Enter Year the book: ").strip())
        self.borrowed = bool(input("Enter Borrowed the book (True/False)").strip().capitalize())
        self.cursor.execute(f"UPDATE books SET title=?, author=?, year=? WHERE id={self.id}", (self.title, self.author, self.year))
        self.conn.commit()
        print(f"This ID: '{self.id}' edit successfully")

    def delete_book(self):
        print("""
                        Delete book
            """)
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        if not self.books:
            print("No books in library")
            return
        self.view_All_Books()
        self.id = int(input("Enter ID book for Delete: "))
        self.cursor.execute(f"DELETE FROM books WHERE id = {self.id}")
        self.conn.commit()
        print(f"This book number ID: '{self.id}' deleted successfully")

    def borroweing_book(self):
        print("""
                        Borrowing Book
            """)
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        if not self.books:
            print("No books in library")
            return
        self.view_All_Books()
        self.id = int(input("Enter the ID of the book you want to borrowing: "))
        self.cursor.execute("SELECT book_id FROM borrowed_books")
        self.books = self.cursor.fetchall()
        for self.book in self.books:
            if self.id == self.book:
                print(f"This book ID: '{self.id}' borroweded, you can borrowed the book after available")
                return
        self.name = input("Enter your name: ").strip().capitalize()
        self.cursor.execute("SELECT user_id, name FROM users")
        self.users = self.cursor.fetchall()
        for self.user in self.users:
            if self.name == self.user[1]:
                self.cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)", (self.user[0], self.id))
                self.cursor.execute(f"UPDATE books SET borrowed = 0 WHERE id = {self.id}")
                self.conn.commit()
                print("The book has been successfully borrowed.")
            else:
                print("There is no book by this name in the library.")

    def returning_book(self):
        print("""
                        Returning Book
            """)
        self.cursor.execute("SELECT * FROM borrowed_books")
        self.bors = self.cursor.fetchall()
        if not self.bors:
            print("No borroweded")
            return
        self.name = input("Enter your name: ").strip().capitalize()
        self.cursor.execute("SELECT user_id, name FROM users")
        self.users = self.cursor.fetchall()
        for self.user in self.users:
            if self.name == self.user[1]:
                self.cursor.execute("SELECT user_id, book_id, id FROM borrowed_books")
                self.ids = self.cursor.fetchall()
                for self.id in self.ids:
                    self.cursor.execute("SELECT * FROM books")
                    self.books = self.cursor.fetchall()
                    for self.i, self.book in enumerate(self.books, start=1):
                        if self.id[1] == self.book[0]:
                            print("View books it borroweded")
                            print(f"{self.i}- ID: {self.book[0]} Title: {self.book[1]} Author: {self.book[2]} Year: {self.book[3]}")
                    else:
                        print("No book borroweded for you")
                        return
            else:
                print("There is no borrowed book to return.")
                return
        self.book_id = int(input("Enter ID book it returning: "))
        for self.id in self.ids:
            if self.book_id == self.id[1]:
                self.cursor.execute(f"DELETE FROM borrowed_books WHERE id = {self.id[2]}")
                self.cursor.execute(f"UPDATE books SET borrowed = 1 WHERE id = {self.id[1]}")
        self.conn.commit()
        print("This book it Returned")

    def Viewing_borrowed_books(self):
        print("""
                        Views All Books in Borrowed
            """)
        self.cursor.execute("SELECT book_id FROM borrowed_books")
        self.book_ids = self.cursor.fetchone()
        if self.book_ids:
            for self.book_id in self.book_ids:
                self.cursor.execute("SELECT * FROM books")
                self.books = self.cursor.fetchall()
                for self.i, self.book in enumerate(self.books, start=1):
                    if self.book_id  == self.book[0]:
                        print(f"{self.i}- ID: {self.book[0]} Title: {self.book[1]} Author: {self.book[2]} Year: {self.book[3]}")
                        return
        else:
            print("No book in borrowed")

    def search_book(self):
        print("""
                        Search Book By Title
            """)
        self.title = input("Enter Title Book For Search: ")
        self.cursor.execute("SELECT * FROM books")
        self.books = self.cursor.fetchall()
        if self.books:
            for self.i, self.book in enumerate(self.books, start=1):
                if self.title == self.book[1]:
                    print(f"{self.i}- ID: {self.book[0]} Title: {self.book[1]} Author: {self.book[2]} Year: {self.book[3]}")
                    return
        else:
            print("No book of the title")
            return
    
    def run(self):
        while True:
            self.show_choices()
            if self.choice == 1:
                self.view_All_Books()
            elif self.choice == 2:
                self.add_book()
            elif self.choice == 3:
                self.edit_book()
            elif self.choice == 4:
                self.delete_book()
            elif self.choice == 5:
                self.borroweing_book()
            elif self.choice == 6:
                self.returning_book()
            elif self.choice == 7:
                self.Viewing_borrowed_books()
            elif self.choice == 8:
                self.search_book()
            elif self.choice == 9:
                self.sing_choices()
                break
            else:
                print("Choice is not found, please choice round (1-10)")

start = Library()
start.sign_choices()
