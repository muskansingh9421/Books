"""Configuration."""

import os
from tempfile import mkdtemp


class Config:
    """Class to set configurations."""

    # General config
    SECRET_KEY = "SECRECTKEY"
    TEMPLATES_AUTO_RELOAD = True

    # Database
    DATABASE_URL = "sqlite:///book.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
