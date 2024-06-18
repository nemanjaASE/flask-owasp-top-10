from app.models.post import Category

def get_all_categories():
    return Category.query.all();

def get_category_by_name(name):
    return Category.query.filter_by(name=name).first()