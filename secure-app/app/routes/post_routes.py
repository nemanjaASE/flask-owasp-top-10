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

    category_service = current_app.category_service
    post_service = current_app.post_service

    try:
        form.category.choices = [(category.id, category.name) for category in category_service.get_all_categories()]
    
        if form.validate_on_submit():
            selected_categories = form.category.data
       
            categories = []
            for category_id in selected_categories:
                category = category_service.get_category_by_id(category_id)
                if category:
                    categories.append(category)

            post_dto = CreatePostDTO(
                title=form.title.data,
                body=form.content.data,
                user_id=current_user.id,
                categories=categories
            )

            post_service.create_post(post_dto)
            return redirect(url_for('main.index'))
    except EntityNotFoundError as e:
            current_app.logger.error('Post not found: %s', (str(e),))
    except DatabaseServiceError as e:
            current_app.logger.error('Database: %s', (str(e),))
    except Exception as e:
            current_app.logger.error('Unhandled: %s', (str(e),))

    return render_template('add_post.html', form=form)

@post_bp.route('/post_details/<string:post_id>')
@login_required
def post_details(post_id):
    post_service = current_app.post_service

    try:
        post = post_service.get_post(post_id);
    except EntityNotFoundError as e:
        current_app.logger.error('Post not found: %s', (str(e),))
    except DatabaseServiceError as e:
        current_app.logger.error('Database: %s', (str(e),))
    except Exception as e:
        current_app.logger.error('Unhandled: %s', (str(e),))


    return render_template('post_details.html',post=post);