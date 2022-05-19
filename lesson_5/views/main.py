from flask import Blueprint, render_template
from flask_login import login_required

from lesson_5.models import Blog

main_app = Blueprint('main_app', __name__)


@main_app.route('/')
@login_required
def home():
    all_blogs = Blog.query.order_by(Blog.id.desc()).paginate(per_page=10)
    return render_template('main/home.html', all_blogs=all_blogs)


@main_app.route('/about/')
@login_required
def about():
    return render_template('main/about.html')
