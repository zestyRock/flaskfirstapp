import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy
from . import db


# app.config['SQLALCHEMY_DATABASE_URI'] = ''


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False)
    content = db.Column(db.Text, unique=False)
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