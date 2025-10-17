"""
Provides CRUD operations for SettingsModel using SQLAlchemy.
"""
from sqlalchemy.orm import Session
from src.models.settings_model import SettingsModel


class SettingsService:
    """
    Service for managing application settings.
    Ensures only one row of settings exists.
    """

    def __init__(self, session: Session):
        self.session = session

    def get_settings(self) -> SettingsModel:
        """
        Returns current settings or creates defaults if none exist.
        """
        settings = self.session.query(SettingsModel).first()
        if not settings:
            settings = SettingsModel(default_download_path="C:/Downloads")
            self.session.add(settings)
            self.session.commit()
            self.session.refresh(settings)
        return settings

    def update_settings(self, **kwargs) -> SettingsModel:
        """
        Updates one or more settings fields.
        Example: update_settings(theme='dark', default_quality='1080p')
        """
        settings = self.get_settings()
        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        self.session.commit()
        self.session.refresh(settings)
        return settings
