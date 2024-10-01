"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=False, default='https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png')

    # In case a user gets delete, their posts will be deleted as well, 
    # also if a post isnt tied to a user, it will be deleted
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')
    
    @classmethod
    def get_all_users(cls):
        """Return all users."""
        return cls.query.all()

    def __repr__(self):
        """Show info about user."""
        fullName = self.get_full_name()
        return f"<User {fullName}>"
    
    def get_full_name(self):
            """Return full name of user."""
            return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    """Post."""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    def __repr__(self):
        """Show info about post."""
        return f"<Post {self.title}, User: {self.user_id}>"

class PostTag(db.Model):
    """PostTag."""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

class Tag(db.Model):
    """Tag."""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    