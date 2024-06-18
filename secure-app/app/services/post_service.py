from app import db
from app.models.post import Post

def get_all_posts():
    return Post.query.all()

def get_post_by_id(post_id):
    return Post.query.filter_by(id=post_id).first();

def add_post(title, body, user_id, categories):
    new_post = Post(title=title, body=body, user_id=user_id, categories=categories)
    db.session.add(new_post)
    db.session.commit()

def posts_count():
    return Post.query.count()