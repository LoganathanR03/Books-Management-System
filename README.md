# Book Management System

## Overview
The **Book Management System** is a Python-based application that allows users to manage books efficiently. It uses **MySQL** as the backend database and **pandas** for data manipulation and analysis. Users can perform operations such as adding new books, updating existing book details, deleting books, and viewing book information in a structured format.

## Features
- Add new books to the database.
- Update book details (title, author, price, quantity, etc.).
- Delete books from the database.
- View all books in a tabular format using pandas.
- Search for books by title or author.
- Generate reports or summaries of book data.

## Tech Stack
- **Programming Language:** Python
- **Database:** MySQL
- **Libraries:** 
  - `mysql-connector-python` for MySQL operations
  - `pandas` for data handling
  - `datetime` for date operations

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>


2. Install required Python packages:

   ```bash
   pip install mysql-connector-python pandas
   ```
3. Make sure MySQL is installed and running on your system.
4. Create a database named `book_management` and a table named `books` with the following structure:

   ```sql
   CREATE TABLE books (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       author VARCHAR(255) NOT NULL,
       price FLOAT NOT NULL,
       quantity INT NOT NULL,
       published_date DATE
   );
   ```

## Usage

1. Update the database connection details in the Python script:

   ```python
   host='localhost',
   database='book_management',
   user='root',
   password='your_password'
   ```
2. Run the Python script:

   ```bash
   python book_management_system.py
   ```
3. Follow the on-screen prompts to add, update, delete, or view books.

## Sample Output

```
+----+----------------------+-----------------+-------+----------+---------------+
| ID | Title                | Author          | Price | Quantity | Published Date|
+----+----------------------+-----------------+-------+----------+---------------+
| 1  | Python Basics        | John Doe        | 250   | 10       | 2023-05-01    |
| 2  | Data Science Handbook| Jane Smith      | 450   | 5        | 2022-11-15    |
+----+----------------------+-----------------+-------+----------+---------------+
```

## Contributing

Feel free to contribute by:

* Adding new features (e.g., CSV import/export)
* Improving the UI
* Enhancing error handling and validations

## License

This project is licensed under the MIT License.

## Contact

For any queries or suggestions, contact me at `logangreen1210@gmail.com`.

```
