"""
This module defines the ListService class responsible for managing
movie download entries in the database using SQLAlchemy.

It provides methods to add, retrieve, list, update, and delete movie items.
"""

from sqlalchemy.orm import Session
from src.models.list_model import ListModel

class ListService:
    """
    Service class for managing movie download entries in the database.

    This class provides methods to perform CRUD operations on the ListModel,
    including adding new entries, retrieving specific entries, listing all,
    listing only active or completed entries, updating fields, marking entries
    as completed, and deleting entries.

    Attributes:
        session (Session): SQLAlchemy session used for database operations.
    """
    def __init__(self, session: Session):
        """
        Initializes the service with the given SQLAlchemy session.

        Args:
            session (Session): SQLAlchemy session object used to interact with the database.
        """
        self.session = session

    def add_item(self, title: str, link: str, quality: str, output_format: str) -> ListModel:
        """
        Adds a new movie to download to the database.

        Args:
            title (str): Title or name of the movie.
            link (str): URL associated with the movie.
            quality (str): Desired download quality.
            output_format (str): Desired output format.

        Returns:
            ListModel: The created ListModel object with all fields populated.
        """
        item = ListModel(
            title=title,
            link=link,
            quality=quality,
            output_format=output_format
        )
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def get_item(self, item_id: int) -> ListModel | None:
        """
        Retrieves a movie entry by its ID.

        Args:
            item_id (int): ID of the movie entry.

        Returns:
            ListModel | None: The corresponding ListModel object if found, otherwise None.
        """
        return self.session.query(ListModel).get(item_id)

    def list_all(self) -> list[ListModel]:
        """
        Returns a list of all movie entries.

        Returns:
            list[ListModel]: A list of all movie entries in the database.
        """
        return self.session.query(ListModel).all()

    def list_active(self) -> list[ListModel]:
        """
        Returns a list of movie entries that are not completed.

        Returns:
            list[ListModel]: Pending movie entries.
        """
        return self.session.query(ListModel).filter_by(completed=False).all()

    def list_completed(self) -> list[ListModel]:
        """
        Returns a list of movie entries that have been completed.

        Returns:
            list[ListModel]: Completed movie entries.
        """
        return self.session.query(ListModel).filter_by(completed=True).all()
    
    def update_item(self, item_id: int, **kwargs) -> bool:
        """
        Updates fields of an existing movie entry.

        Args:
            item_id (int): ID of the movie entry.
            **kwargs: Fields to update (title, link, quality, output_format, completed).

        Returns:
            bool: True if update was successful, False if the item does not exist.
        """
        item = self.get_item(item_id)
        if not item:
            return False
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        self.session.commit()
        return True

    def mark_completed(self, item_id: int) -> bool:
        """
        Marks a movie entry as completed.

        Args:
            item_id (int): ID of the movie entry.

        Returns:
            bool: True if the update was successful, False if the item does not exist.
        """
        return self.update_item(item_id, completed=True)

    def delete_item(self, item_id: int) -> bool:
        """
        Deletes a movie entry from the database.

        Args:
            item_id (int): ID of the movie entry to delete.

        Returns:
            bool: True if the deletion was successful, False if the item does not exist.
        """
        item = self.get_item(item_id)
        if not item:
            return False
        self.session.delete(item)
        self.session.commit()
        return True