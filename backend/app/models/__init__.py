from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .photo import Photo
from .album import Album
from .moment import Moment
from .user import User
