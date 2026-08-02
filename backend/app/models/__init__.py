from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .photo import Photo
from .album import Album
from .user import User
