"""
Defines the SettingsModel ORM class, storing application configuration.
"""

from sqlalchemy import Column, Integer, String
from src.models.base import Base


class SettingsModel(Base):
    """
    ORM model for storing user/application settings.
    """
    __tablename__ = "settings_model"

    id = Column(Integer, primary_key=True, autoincrement=True)
    theme = Column(String, default="light", nullable=False)  # light / dark
    default_quality = Column(String, default="The best", nullable=False)
    default_video_format = Column(String, default="mp4", nullable=False)
    default_audio_format = Column(String, default="mp3", nullable=False)
    default_download_path = Column(String, nullable=False)

    def __repr__(self):
        return (
            f"<SettingsModel(theme='{self.theme}', quality='{self.default_quality}', "
            f"video='{self.default_video_format}', audio='{self.default_audio_format}', "
            f"path='{self.default_download_path}')>"
        )
