from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from .models import db, Post
from flask import current_app as app


# def get_post(post_id):
#     conn = get_db_connection()

#     post = conn.execute('SELECT * FROM posts WHERE id = ?', [post_id]).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post



@app.route('/')
def index():
    return render_template('index.html', posts=Post.query.all())
    
# @app.route('/create', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         else: 
#             conn = get_db_connection()
#             conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
#                          (title, content))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))

#     return render_template('create_post.html')


# @app.route('/<int:post_id>')
# def post(post_id):
#     post = get_post(post_id)
#     return render_template('post.html', post=post)

# @app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
# def edit(post_id):
#     post = get_post(post_id)

#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         else:
#             conn = get_db_connection()
#             conn.execute('UPDATE posts SET title = ?, content = ?'
#                          ' WHERE id = ?',
#                          (title, content, post_id))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))
#     return render_template('edit.html', post=post)


# @app.route('/<int:post_id>/delete', methods=('POST',))
# def delete(post_id):
#     post = get_post(post_id)
#     conn = get_db_connection()
#     conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
#     conn.commit()
#     conn.close()
#     flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('index'))  

