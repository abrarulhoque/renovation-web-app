import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional


class Database:
    """
    Database service for storing and retrieving form submissions.
    """

    def __init__(self, db_path: str = "renovation_quotes.db"):
        """
        Initialize the database connection.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._create_tables_if_not_exist()

    def _get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)

    def _create_tables_if_not_exist(self):
        """Create the necessary tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Check if workorder_paths column exists
        cursor.execute("PRAGMA table_info(quotes)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Create quotes table if it doesn't exist
        if not columns:
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                floor_area REAL,
                document_path TEXT,
                form_data TEXT,
                workorder_paths TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            )
        # Alter the table to add workorder_paths column if it doesn't exist
        elif "workorder_paths" not in column_names:
            cursor.execute("ALTER TABLE quotes ADD COLUMN workorder_paths TEXT")

        conn.commit()
        conn.close()

    def add_quote(
        self,
        customer_name: str,
        email: str,
        phone: str,
        address: str,
        floor_area: float,
        document_path: str,
        form_data: Dict[str, Any],
        workorder_paths: List[str] = None,
    ) -> int:
        """
        Add a new quote to the database.

        Args:
            customer_name: Name of the customer
            email: Email address of the customer
            phone: Phone number of the customer
            address: Address of the customer
            floor_area: Floor area of the bathroom
            document_path: Path to the generated document
            form_data: JSON serializable dictionary of form data
            workorder_paths: List of paths to generated workorder PDFs

        Returns:
            The ID of the newly created quote
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO quotes 
            (customer_name, email, phone, address, floor_area, document_path, form_data, workorder_paths) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer_name,
                email,
                phone,
                address,
                floor_area,
                document_path,
                json.dumps(form_data),
                json.dumps(workorder_paths) if workorder_paths else None,
            ),
        )

        quote_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return quote_id

    def get_all_quotes(self) -> List[Dict[str, Any]]:
        """
        Get all quotes from the database.

        Returns:
            A list of dictionaries containing quote data
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, customer_name, email, phone, address, floor_area, 
                   document_path, workorder_paths, created_at 
            FROM quotes 
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()
        quotes = []

        for row in rows:
            quote = dict(row)
            # Parse workorder_paths from JSON if it exists
            if quote["workorder_paths"]:
                try:
                    quote["workorder_paths"] = json.loads(quote["workorder_paths"])
                except json.JSONDecodeError:
                    quote["workorder_paths"] = []
            else:
                quote["workorder_paths"] = []

            quotes.append(quote)

        conn.close()

        return quotes

    def get_quote_by_id(self, quote_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a quote by its ID.

        Args:
            quote_id: The ID of the quote to retrieve

        Returns:
            A dictionary containing quote data, or None if not found
        """
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, customer_name, email, phone, address, floor_area, 
                   document_path, form_data, workorder_paths, created_at 
            FROM quotes 
            WHERE id = ?
            """,
            (quote_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            quote = dict(row)
            # Parse form_data from JSON
            quote["form_data"] = json.loads(quote["form_data"])

            # Parse workorder_paths from JSON if it exists
            if quote["workorder_paths"]:
                try:
                    quote["workorder_paths"] = json.loads(quote["workorder_paths"])
                except json.JSONDecodeError:
                    quote["workorder_paths"] = []
            else:
                quote["workorder_paths"] = []

            return quote

        return None

    def delete_quote(self, quote_id: int) -> bool:
        """
        Delete a quote by its ID.

        Args:
            quote_id: The ID of the quote to delete

        Returns:
            True if the quote was deleted, False otherwise
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))

        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return deleted
