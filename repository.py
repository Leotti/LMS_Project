from typing import List, Optional


from database import Database
from model import Book, Publisher, Member
from utils import logger


class Repository:
    """
    Repository class for handling database operations related to books, publishers, members, and loans.
    """

    def __init__(self) -> None:
        """Initializes the Repository class and connects to the database."""
        self.db = Database()
        try:
            self.db.connect()
        except Exception as e:
            logger.critical(f"Failed to connect to the database: {e}")
            raise RuntimeError("Database connection failed.")

    def fetchall_books(self) -> List[Book]:
        """
        Fetches all books from the database.

        Returns:
            List[Book]: A list of Book objects representing all books in the database.
        """
        
        ### YOUR CODE ###
        query = "SELECT book_id, title, author, publisher_id, isbn, year_published FROM book;"

        try:
            results = self.db.fetch_results(query = query)
            return [Book(*result) for result in results]
        except Exception as e:
            logger.error(f"Failed to fetch all books: {e}")
            return []

    def add_book(self, book: Book) -> None:
        """
        Adds a new book to the database.

        Args:
            book (Book): The book object to be added.
        """
        
        ### YOUR CODE ###
        query = "INSERT INTO book (title, author, publisher_id, isbn, year_published) VALUES (%s, %s, %s, %s, %s);"
        params = (str(book.title), str(book.author), book.publisher_id if book.publisher_id else None, str(book.isbn), int(book.year_published))

        try:
            self.db.execute_query(query = query, params = params)
            logger.info(f"Book '{book.title}' added successfully.")
        except Exception as e:
            logger.error(f"Failed to add book '{book.title}': {e}")
            raise RuntimeError("Failed to add book.")

    def delete_book_by_id(self, book_id: int) -> None:
        """
        Deletes a book by its ID.

        Args:
            book_id (int): The ID of the book to delete.
        """
        
        ### YOUR CODE ###
        query = "DELETE FROM book WHERE book_id = %s;"
        params = (book_id,)

        try:
            self.db.execute_query(query = query, params = params)
            logger.info(f"Book with ID {book_id} deleted successfully.")
        except Exception as e:
            logger.error(f"Failed to delete book with ID {book_id}: {e}")
            raise RuntimeError("Failed to delete book.")

    def update_book(self, book: Book) -> None:
        """
        Updates the details of a book in the database.

        Args:
            book (Book): The book object with updated information.
        """
        ### YOUR CODE ###
        query = "UPDATE book SET title = %s, author = %s, publisher_id = %s, year_published = %s WHERE book_id = %s;"
        params = (book.title, book.author, book.publisher_id, book.year_published, book.id)

        try:
            self.db.execute_query(query = query, params = params)
            logger.info(f"Book with ID {book.id} updated successfully.")
        except Exception as e:
            logger.error(f"Failed to update book with ID {book.id}: {e}")
            raise RuntimeError("Failed to update book.")

    def get_books_by_author_name(self, author_name: str) -> List[Book]:
        """
        Fetches books by author name.

        Args:
            author_name (str): The name of the author.

        Returns:
            List[Book]: A list of books by the given author.
        """
        ### YOUR CODE ###
        query = "SELECT book_id, title, author, publisher_id, isbn, year_published FROM book WHERE author = %s;"
        params = (author_name,)

        try:
            results = self.db.fetch_results(query = query, params = params)
            return [Book(*result) for result in results]
        except Exception as e:
            logger.error(f"Failed to fetch books by author '{author_name}': {e}")
            return []

    def get_publishers(self) -> List[Publisher]:
        """
        Fetches all publishers from the database.

        Returns:
            List[Publisher]: A list of Publisher objects.
        """
        ### YOUR CODE ###
        query = "SELECT publisher_id, name, address, phone, email FROM publisher;"

        try:
            results = self.db.fetch_results(query = query)
            return [Publisher(*result) for result in results]
        except Exception as e:
            logger.error(f"Failed to fetch publishers: {e}")
            return []

    def get_all_members(self) -> List[Member]:
        """
        Fetches all members from the database.

        Returns:
            List[Member]: A list of Member objects.
        """
        ### YOUR CODE ###
        query = "SELECT member_id, first_name, last_name, email, phone, address, date_of_membership FROM member;"


        try:
            results = self.db.fetch_results(query = query)
            return [Member(*result) for result in results]
        except Exception as e:
            logger.error(f"Failed to fetch members: {e}")
            return []

    def get_book_by_name(self, book_name: str) -> Optional[Book]:
        """
        Fetches a book by its title.

        Args:
            book_name (str): The title of the book.

        Returns:
            Optional[Book]: The Book object if found, otherwise None.
        """
        ### YOUR CODE ###
        query = "SELECT book_id, title, author, publisher_id, isbn, year_published FROM book WHERE title = %s LIMIT 1;"
        params = (book_name,)

        try:
            result = self.db.fetch_results(query = query, params = params)
            return Book(*result[0]) if result else None
        except Exception as e:
            logger.error(f"Failed to fetch book '{book_name}': {e}")
            return None

    def get_all_members_by_book(self, book_name: str) -> List[tuple]:
        """
        Fetches all members who borrowed a specific book.

        Args:
            book_name (str): The title of the book.

        Returns:
            List[tuple]: A list of tuples containing member and loan information.
        """
        book = self.get_book_by_name(book_name)
        if not book:
            logger.warning(f"No book found with title '{book_name}'.")
            return []
        ### YOUR CODE ###
        query = """
            SELECT m.first_name, m.last_name, b.title, l.date_borrowed, l.due_date, l.date_returned
            FROM member m
            JOIN loan l ON m.member_id = l.member_id
            JOIN book b ON l.book_id = b.book_id
            WHERE b.title = %s;
        """
        params = (book_name,)

        try:
            return self.db.fetch_results(query = query, params = params)
        except Exception as e:
            logger.error(f"Failed to fetch members for book '{book_name}': {e}")
            return []

    def get_all_loans(self) -> List[tuple]:
        """
        Fetches all loans from the database.

        Returns:
            List[tuple]: A list of tuples containing loan information.
        """
        ### YOUR CODE ###
        query = """
            SELECT DISTINCT m.first_name, m.last_name, b.title, l.date_borrowed, l.due_date, l.date_returned
            FROM member m
            JOIN loan l ON m.member_id = l.member_id
            JOIN book b ON l.book_id = b.book_id;
        """
        
        try:
            return self.db.fetch_results(query = query)
        except Exception as e:
            logger.error(f"Failed to fetch loans: {e}")
            return []
