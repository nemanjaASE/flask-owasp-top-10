from flask import render_template, redirect, url_for, current_app
from flask_login import login_required, current_user

from app.forms.post_form import PostForm
from app.dto.create_post_dto import CreatePostDTO
from app import requires_roles 

from app.services.exceptions import *

from . import post_bp

@post_bp.route('/add_post', methods=['GET', 'POST'])
@login_required
@requires_roles('Admin', 'Author')
def add_post():
    form = PostForm()


    form.category.choices = [(category.id, category.name) for category in current_app.category_service.get_all_categories()]
    
    if form.validate_on_submit():
        selected_categories = form.category.data
       
        categories = []
        for category_id in selected_categories:
            category = current_app.category_service.get_category_by_id(category_id)
            if category:
                categories.append(category)

                post_dto = CreatePostDTO(
                    title=form.title.data,
                    body=form.content.data,
                    user_id=current_user.id,
                    categories=categories
                )

        current_app.post_service.create_post(post_dto)
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                current_app.security_logger.log_invalid_input(field, error)

    return render_template('add_post.html', form=form)

@post_bp.route('/post_details/<string:post_id>')
@login_required
def post_details(post_id):
    post = current_app.post_service.get_post(post_id);
    return render_template('post_details.html',post=post);