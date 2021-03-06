#!/usr/bin/env python
#encoding:utf-8
__author__ = 'Samren'
from flask import jsonify, url_for, request, g, current_app
from ..models import Post, Permission
from .. import db
from .decorators import permission_required
from .errors import forbidden
from . import api


@api.route('/posts/', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page+1, _external=True)
    post_list = [post.to_json() for post in posts]
    return jsonify({
        'posts': post_list,
        'prev_page': prev_page,
        'next_page': next_page,
        'total_count': pagination.total,
        'page_count': post_list.__len__()
    })


@api.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post',
                             id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())