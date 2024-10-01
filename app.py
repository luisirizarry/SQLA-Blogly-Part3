"""Blogly application."""

from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """Home page"""
    return redirect('/users')

# User routes

@app.route('/users')
def list_users():
    """List all users"""
    users = User.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Show form to create new user"""
    return render_template('create_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Create new user"""
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageURL']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Show form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edit user"""
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageURL']

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

# Post routes

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form to create new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all() 
    return render_template('post_form.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def post_user_post(user_id):
    """Create new post and redirect back to users page"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tags')

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    new_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(post_id, user_id):
    """Show post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edit post"""
    title = request.form['title']
    content = request.form['content']
    tag_ids = request.form.getlist('tags')

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)  # Delete the post
    db.session.commit()  # Commit the changes
    return redirect(f'/users/{user.id}')  # Redirect to the user's page

# Tag routes

@app.route('/tags')
def list_tags():
    """List all tags"""
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/new', methods=["GET"])
def show_tag_form():
    """Show form to create new tag"""
    return render_template('create_tag.html')

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Create new tag"""
    name = request.form['tagName']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_form(tag_id):
    """Show form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Edit tag"""
    name = request.form['tagName']
    tag = Tag.query.get_or_404(tag_id)
    tag.name = name
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    Tag.query.filter(Tag.id == tag_id).delete()
    db.session.commit()
    return redirect('/tags')
    


