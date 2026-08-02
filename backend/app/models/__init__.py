from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .photo import Photo
from .album import Album
from .todo import Todo
from .user import User
