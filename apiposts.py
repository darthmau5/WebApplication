from flask import Blueprint, jsonify, request
from app.models import Post, User
from app import db

api = Blueprint('api', __name__)

@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    output = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'date_posted': post.date_posted
        }
        output.append(post_data)
    return jsonify({'posts': output})

@api.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'date_posted': post.date_posted
    })

@api.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = Post(
        title=data['title'],
        content=data['content'],
        author=User.query.get(data['user_id'])
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'New post created!'}), 201