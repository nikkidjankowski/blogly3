from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

"""Blogly application."""



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "HI"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
toolbar = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def list():
    """shows pet page"""
   
    return redirect("/user")


@app.route('/user', methods=["GET"])
def list_users():
    """shows pet page"""
    users = User.query.all()
    return render_template('user/showuser.html', users=users)

@app.route('/user/newuser', methods=["GET"])
def open_create_user():
    

    return render_template("user/createnewuser.html")

@app.route('/user/newuser', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    
    

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/user')

@app.route("/user/<int:user_id>", methods=["GET"])
def show_user(user_id):
    """show details about single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("user/userprofile.html", user=user, user_id=user_id)

@app.route("/user/<int:user_id>/edit", methods=["GET"])
def get_edit_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('user/edit.html', user=user)



@app.route("/user/<int:user_id>/edit", methods=["POST"])
def post_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect("/user")


@app.route("/user/<int:user_id>/posts/new", methods=["GET"])
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('posts/new.html', user=user, tags=tags)

@app.route("/user/<int:user_id>/posts/new", methods=["POST"])
def get_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    print("HERE")
    print(tag_ids)
    print(tags)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/user/{user_id}")


@app.route("/posts/<int:post_id>", methods=["GET"])
def show_certain_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_certain_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit2.html', post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def submit_certain_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    print("THIS IS POST/ID/EDIT", tag_ids)
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/user/{post.user_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect(f"/user/{post.user_id}")


@app.route("/tags", methods=["GET"])
def show_tags():
    tags = Tag.query.all()
    return render_template('tags/showtags.html', tags=tags)

@app.route("/tags/new", methods=["GET"])
def tag_form():
    posts = Post.query.all()
    return render_template('tags/createtag.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def post_tag_form():
    
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    new_tag = Tag(name=request.form['name'], posts=posts)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>", methods=["GET"])
def tag_info(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('tags/taginfo.html', tag=tag)



@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def edit_certain_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    print("THIS IS THE posts in tag", posts)
    return render_template('tags/edit.html', posts=posts, tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_certain_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    print("THIS IS POST/ID/EDIT", post_ids)
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")