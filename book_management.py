import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import pandas as pd

class BookManagementSystem:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='book_management',
                user='root',
                password='13572468'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    
        

    # Book Operations
    def add_book(self, title, author, isbn, genre=None, publication_year=None, quantity=1):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO books 
                       (title, author, isbn, genre, publication_year, quantity) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (title, author, isbn, genre, publication_year, quantity))
            self.connection.commit()
            print(f"Book '{title}' added successfully")
        except Error as e:
            print(f"Error adding book: {e}")

    def get_all_books(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()  # Save the results first
    
            if books:
                df_allbooks = pd.DataFrame(books)
                print("\n📚 List of Books:\n")
                print(df_allbooks.to_string(index=False))  # Pretty printed table
            else:
                print("No books found.")
    
            
        except Error as e:
            print(f"Error fetching books: {e}")
            return []


    def search_books(self, search_term):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """SELECT * FROM books 
                       WHERE title LIKE %s OR author LIKE %s OR isbn LIKE %s"""
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            searchbook = cursor.fetchall()
            if searchbook:
                df_searchbook = pd.DataFrame(searchbook)
                print("\n📚 List of Books:\n")
                print(df_searchbook.to_string(index=False))
            else:
                print("No books found.")
        except Error as e:
            print(f"Error searching books: {e}")
            return []

    def update_book(self, book_id, **kwargs):
        try:
            cursor = self.connection.cursor()
            set_clause = ", ".join([f"{key}=%s" for key in kwargs])
            values = list(kwargs.values())
            values.append(book_id)
            
            query = f"UPDATE books SET {set_clause} WHERE id=%s"
            cursor.execute(query, values)
            self.connection.commit()
            print(f"Book ID {book_id} updated successfully")
        except Error as e:
            print(f"Error updating book: {e}")

    def delete_book(self, book_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            self.connection.commit()
            print(f"Book ID {book_id} deleted successfully")
        except Error as e:
            print(f"Error deleting book: {e}")

    # User Operations
    def add_user(self, username, password, email=None, is_admin=False):
        try:
            cursor = self.connection.cursor()
            query = """INSERT INTO users 
                       (username, password, email, is_admin) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (username, password, email, is_admin))
            self.connection.commit()
            print(f"User '{username}' added successfully")
        except Error as e:
            print(f"Error adding user: {e}")

    def authenticate_user(self, username, password):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            return cursor.fetchone()
        except Error as e:
            print(f"Error authenticating user: {e}")
            return None

    # Borrow/Return Operations
    def borrow_book(self, book_id, user_id, days=14):
        try:
            # Check book availability
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT quantity FROM books WHERE id=%s", (book_id,))
            book = cursor.fetchone()
            
            if not book or book['quantity'] < 1:
                print("Book not available for borrowing")
                return False
            
            # Update book quantity
            cursor.execute("UPDATE books SET quantity=quantity-1 WHERE id=%s", (book_id,))
            
            # Create borrow record
            borrow_date = datetime.now().date()
            due_date = borrow_date + timedelta(days=days)
            
            query = """INSERT INTO borrowed_books 
                       (book_id, user_id, borrow_date, due_date) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (book_id, user_id, borrow_date, due_date))
            self.connection.commit()
            print("Book borrowed successfully")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"Error borrowing book: {e}")
            return False

    def return_book(self, borrow_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get borrow record
            cursor.execute("SELECT book_id FROM borrowed_books WHERE id=%s AND return_date IS NULL", (borrow_id,))
            record = cursor.fetchone()
            
            if not record:
                print("No active borrowing record found")
                return False
            
            # Update book quantity
            cursor.execute("UPDATE books SET quantity=quantity+1 WHERE id=%s", (record['book_id'],))
            
            # Update borrow record
            return_date = datetime.now().date()
            cursor.execute("UPDATE borrowed_books SET return_date=%s WHERE id=%s", (return_date, borrow_id))
            
            self.connection.commit()
            print("Book returned successfully")
            return True
        except Error as e:
            self.connection.rollback()
            print(f"Error returning book: {e}")
            return False

    def get_borrowed_books(self, user_id=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if user_id:
                query = """SELECT b.title, b.author, bb.borrow_date, bb.due_date 
                           FROM borrowed_books bb
                           JOIN books b ON bb.book_id = b.id
                           WHERE bb.user_id=%s AND bb.return_date IS NULL"""
                cursor.execute(query, (user_id,))
            else:
                query = """SELECT b.title, u.username, bb.borrow_date, bb.due_date 
                           FROM borrowed_books bb
                           JOIN books b ON bb.book_id = b.id
                           JOIN users u ON bb.user_id = u.id
                           WHERE bb.return_date IS NULL"""
                cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Error fetching borrowed books: {e}")
            return []

    def admin(self, user_record):
        while True:
                print("\nAdmin Menu:")
                print("1. Add Book")
                print("2. Update Book")
                print("3. Delete Book")
                print("4. Add User")
                print("5. View All Books")
                print("6. Search Books")
                print("7. Exit")
                choice = input("Choose an option: ")

                if choice == "1":
                    title = input("Title: ")
                    author = input("Author: ")
                    isbn = input("ISBN: ")
                    genre = input("Genre: ")
                    year = input("Publication Year: ")
                    quantity = input("Quantity: ")
                    system.add_book(title, author, isbn, genre, int(year), int(quantity))
                elif choice == "2":
                    book_id = int(input("Book ID to update: "))
                    field = input("Field to update (title, author, isbn, genre, publication_year, quantity): ")
                    value = input(f"New value for {field}: ")
                    system.update_book(book_id, **{field: value})
                elif choice == "3":
                    book_id = int(input("Book ID to delete: "))
                    system.delete_book(book_id)
                elif choice == "4":
                    uname = input("New Username: ")
                    pwd = input("Password: ")
                    email = input("Email (optional): ")
                    is_admin = input("Is Admin? (yes/no): ").lower() == "yes"
                    system.add_user(uname, pwd, email, is_admin)
                elif choice == "5":
                    books = system.get_all_books()
                elif choice == "6":
                    term = input("Enter title/author/ISBN to search: ")
                    results = system.search_books(term)
                elif choice == "7":
                    print("Goodbye Admin!")
                    break
                else:
                    print("Invalid option. Try again.")
    def user(self, user_record):
        while True:
            print("\nUser Menu:")
            print("1. View All Books")
            print("2. Search Books")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                books = system.get_all_books()
                for book in books:
                    print(book)
            elif choice == "2":
                term = input("Enter title/author/ISBN to search: ")
                results = system.search_books(term)
                
            elif choice == "3":
                book_id = int(input("Enter Book ID to borrow: "))
                system.borrow_book(book_id, user_record['id'])
            elif choice == "4":
                borrow_id = int(input("Enter Borrow ID to return: "))
                system.return_book(borrow_id)
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again.")
        
         

    #user verification
    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user_record = self.authenticate_user(username, password)

        if user_record:
            print(f"\n✅ Login successful! Welcome, {user_record['username']}.")
            if user_record['is_admin']:
                print("🛠️  Admin Access Granted.")
                self.admin(user_record)
            else:
                print("👤 Logged in as User.")
                self.user(user_record)
        else:
            print("❌ Login failed. Incorrect username or password.")
            self.login()


# Program starts here!
if __name__ == "__main__":
    system = BookManagementSystem()
    
    print("""
    Welcome to Books Management System
    ``````` `` ````` `````````` ``````
    """)
    system.login()

    

        
        
            
