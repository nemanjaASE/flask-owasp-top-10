from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.services import post_service, category_service
from app.forms.post_form import PostForm

from . import post_bp

@post_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    form.category.choices = [(category.id, category.name) for category in category_service.get_all_categories()]
    
    if form.validate_on_submit():
        selected_categories = form.category.data
        categories = []
        for category_name in selected_categories:
            category = category_service.get_category_by_name(category_name)
            if category:
                categories.append(category)
        
        post_service.add_post(form.title.data, form.content.data, current_user.id, categories)
        return redirect(url_for('main.index'))
    
    return render_template('add_post.html', form=form)

@post_bp.route('/post_details/<int:post_id>')
@login_required
def post_details(post_id):
    post = post_service.get_post_by_id(post_id);
    return render_template('post_details.html',post=post);