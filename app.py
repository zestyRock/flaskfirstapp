import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:gy198912@localhost/smartcontent_local'
db = SQLAlchemy(app)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False)
    content = db.Column(db.String(128), unique=False)
    score = db.Column(db.Integer)
    last_published_platform = db.Column(db.String(200))
  
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_published_time = db.Column(db.DateTime)

    tags = db.relationship('Tag', secondary='post_tags')
    platforms = db.relationship('Platform', secondary='platform_tags')
    
    def __repr__(self):
        return '<Post %r>' % self.title

class Platform(db.Model):
    __tablename__ = 'platform';
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    
    def __repr__(self):
        return '<Tag %r>' % self.name

class Tag(db.Model):
    __tablename__ = 'tag';
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    posts = db.relationship('Post', secondary='post_tags')

    def __repr__(self):
        return '<Tag %r>' % self.name

class PostPlatform(db.Model):
    __tablename__ = 'post_platforms'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), primary_key=True)

class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    # post = db.relationship(Post, backref=db.backref("post", cascade="all, delete-orphan"))
    # tag = db.relationship(Tag, backref=db.backref("tag", cascade="all, delete-orphan"))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()

    post = conn.execute('SELECT * FROM posts WHERE id = ?', [post_id]).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post



@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    post_dict = json.dumps( [dict(p) for p in posts] ) 
    return render_template('index.html', posts=posts)
    # return jsonify(post_dict)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else: 
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create_post.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, post_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = get_post(post_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))  

