"""Seed file to make sample data for users, posts, tags, and post_tags db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

# Add Users
aaron = User(first_name='Aaron', last_name='Smith', image_url='https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png')
maximus = User(first_name='Maximus', last_name='Davis', image_url='https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png')
david = User(first_name='David', last_name='Edison', image_url='https://www.freeiconspng.com/thumbs/profile-icon-png/profile-icon-9.png')

# Add new objects to session, so they'll persist
db.session.add_all([aaron, maximus, david])
db.session.commit()

# Add posts
post1 = Post(title='First Post', content='This is my first post.', user_id=aaron.id)
post2 = Post(title='Second Post', content='This is my second post.', user_id=maximus.id)
post3 = Post(title='Third Post', content='This is my third post.', user_id=david.id)

# Add new objects to session, so they'll persist
db.session.add_all([post1, post2, post3])
db.session.commit()

# Add Tags
tag1 = Tag(name='Fun')
tag2 = Tag(name='Awesome')
tag3 = Tag(name='Interesting')
tag4 = Tag(name='Sigma')

# Add new objects to session, so they'll persist
db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()

# Add PostTags (associations between posts and tags)
post_tag1 = PostTag(post_id=post1.id, tag_id=tag1.id)
post_tag2 = PostTag(post_id=post1.id, tag_id=tag2.id) 
post_tag3 = PostTag(post_id=post2.id, tag_id=tag3.id)  
post_tag4 = PostTag(post_id=post3.id, tag_id=tag4.id)  
post_tag5 = PostTag(post_id=post3.id, tag_id=tag2.id)  

# Add new objects to session, so they'll persist
db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5])
db.session.commit()

print("Seed data has been added successfully.")
