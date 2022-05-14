from functools import wraps

from flask import Blueprint, request, render_template, abort, url_for, redirect, flash
from flask_login import login_required, current_user

from lesson_4.blog_project.models import Blog, User, Comment, db, Tag
from lesson_4.blog_project.forms import CommentForm, BlogForm

blogs_app = Blueprint('blogs_app', __name__)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Only admins can access this page.', category='danger')
            return redirect(url_for('main_app.home'))
        return f(*args, **kwargs)

    return decorated_function


@blogs_app.route('/search/', methods=['GET'])
@login_required
def search_blogs():
    keyword = request.args.get('keyword')
    select = request.args.get('select')
    data = None

    if keyword:
        if select == 'blogs':
            data = Blog.query \
                .filter(Blog.text.like('%' + keyword + '%')).order_by(Blog.title) \
                .paginate(per_page=10)
        else:
            data = User.query \
                .filter(User.username.like('%' + keyword + '%')).order_by(User.username) \
                .paginate(per_page=10)

    return render_template('search.html', keyword=keyword, data=data, select=select)


@blogs_app.route('/blog/<int:blog_id>/', methods=['GET', 'POST'])
@login_required
def get_blog(blog_id):
    form = CommentForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            comment_text = form.text.data
            new_comment = Comment(
                text=comment_text,
                user_id=current_user.id,
                blog_id=blog_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('blogs_app.get_blog', blog_id=blog_id))
    blog = Blog.query.filter_by(id=blog_id).one_or_none()
    comments = Comment.query.filter_by(blog_id=blog_id).order_by(Comment.id.desc())

    return render_template('get_blog.html', blog=blog, form=form, comments=comments)


@blogs_app.route('/add-blog/', methods=['GET', 'POST'])
@login_required
def add_blog():
    tags = Tag.query.all()

    if request.method == 'POST':
        tag_ids = request.form.getlist('tags')
        tags = [Tag.query.filter_by(id=tag_id).one_or_none() for tag_id in tag_ids]
        new_blog = Blog(
            title=request.form.get('title'),
            text=request.form.get('ckeditor'),
            tags=tags,
            user=current_user,
        )
        db.session.add(new_blog)
        db.session.commit()

        flash('The blog has been created.', category='info')
        referrer = request.form.get('referrer')
        if 'user' in referrer:
            return redirect(url_for('accounts_app.get_user_profile', user_id=current_user.id))
        return redirect(url_for('main_app.home'))

    return render_template('add_blog.html', tags=tags)


@blogs_app.route('/edit-blog/<int:blog_id>/', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first_or_404()
    tags = Tag.query.all()
    form = BlogForm()
    if current_user.id == blog.user_id:
        if request.method == 'GET':
            form.text.data = blog.text
        if request.method == 'POST':
            tag_ids = form.tags.data
            tags = [Tag.query.filter_by(id=tag_id).one_or_none() for tag_id in tag_ids]
            blog.title = form.title.data
            blog.text = form.text.data
            blog.tags = tags

            db.session.commit()
            flash('The blog has been edited.', category='info')
            return redirect(url_for('blogs_app.get_blog', blog_id=blog_id))

        return render_template('edit_blog.html', blog=blog, tags=tags, form=form)

    else:
        abort(404)


@blogs_app.route('/all-tags/')
@login_required
@admin_only
def all_tags():
    tags = Tag.query.all()
    return render_template('all_tags.html', tags=tags)


@blogs_app.route('/add-tag/', methods=['GET', 'POST'])
@login_required
@admin_only
def add_tag():
    if request.method == 'POST':
        new_tag = Tag(
            name=request.form.get('name'),
            color=request.form.get('color')[1:],
        )
        db.session.add(new_tag)
        db.session.commit()
        flash('The tag has been successfully created.', category='info')
        return redirect(url_for('blogs_app.all_tags'))

    return render_template('add_tag.html')


@blogs_app.route('/edit-tag/<int:tag_id>/', methods=['GET', 'POST'])
@login_required
@admin_only
def edit_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).one()
    if request.method == 'POST':
        tag.name = request.form.get('name')
        tag.color = request.form.get('color')[1:]
        db.session.commit()
        flash('The tag has been successfully updated.', category='info')
        return redirect(url_for('blogs_app.all_tags'))

    return render_template('edit_tag.html', tag=tag)


@blogs_app.route('/delete-tag/<int:tag_id>/', methods=['GET', 'POST'])
@login_required
@admin_only
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).one()
    if request.method == 'POST':
        db.session.delete(tag)
        db.session.commit()
        return redirect(url_for('blogs_app.all_tags'))

    return render_template('delete_tag.html', tag=tag)
