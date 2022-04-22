import random
from pprint import pprint

from sqlalchemy.orm import Session
from faker import Faker

try:
    from .db_settings import Base, Session
    from .models import User, Tag, Post, Comment
except ImportError:
    from db_settings import Base, Session
    from models import User, Tag, Post, Comment


def create_tables():
    Base.metadata.create_all()


def drop_tables():
    Base.metadata.drop_all()


def add_and_commit(session: Session, new_object):
    session.add(new_object)
    session.commit()
    return new_object


def create_user(session: Session, username, email):
    new_user = User(username=username, email=email)
    return add_and_commit(session, new_user)


def create_tag(session: Session, name):
    new_tag = Tag(name=name)
    return add_and_commit(session, new_tag)


def create_post(session: Session, title, text, tags, user_id):
    new_post = Post(title=title, text=text, tags=tags, user_id=user_id)
    return add_and_commit(session, new_post)


def create_comment(session: Session, text, user_id):
    new_comment = Comment(text=text, user_id=user_id)
    return add_and_commit(session, new_comment)


def populate_fake_data(users_quantity=None, posts_quantity=None, tags_quantity=None, comments_quantity=None):
    session: Session = Session()
    fake = Faker()

    tags = []

    def generate_new_tag():
        new_tag = create_tag(session, fake.user_name())
        tags.append(new_tag)

    if users_quantity:
        for user in range(users_quantity):
            create_user(session, fake.user_name(), fake.ascii_email())
    if tags_quantity:
        for tag in range(tags_quantity):
            generate_new_tag()
    if posts_quantity:
        for post in range(posts_quantity):
            try:
                create_post(
                    session,
                    fake.name(),
                    fake.paragraph(nb_sentences=5),
                    tags,
                    random.randint(1, session.query(User).count())
                )
            except ValueError:
                generate_new_tag()
                create_user(session, fake.user_name(), fake.ascii_email())
    if comments_quantity:
        for comment in range(comments_quantity):
            try:
                create_comment(session, fake.paragraph(nb_sentences=1), random.randint(1, session.query(User).count()))
            except ValueError:
                create_user(session, fake.user_name(), fake.ascii_email())


def main():
    create_tables()
    populate_fake_data(users_quantity=10, posts_quantity=10, tags_quantity=10, comments_quantity=10)

    # session = Session()

    # get_all_posts = session.query(Post).all()
    # pprint(get_all_posts)

    # get_all_users = session.query(User).all()
    # pprint(get_all_users)

    # get_posts_by_a_specific_user = session.query(Post).filter_by(user_id=1).all()
    # pprint(get_posts_by_a_specific_user)

    # get_blogs_starting_with_a = session.query(Post).filter(Post.text.like('a%')).all()
    # if get_blogs_starting_with_a:
    #     pprint(get_blogs_starting_with_a)
    # else:
    #     print('Nothing found.')

    # get_user_by_id = session.get(User, 1)
    # print(get_user_by_id)

    # get_users_username_ending_with_n = session.query(User).filter(User.username.like('%n')).all()
    # if get_users_username_ending_with_n:
    #     pprint(get_users_username_ending_with_n)
    # else:
    #     print('Nothing found.')


if __name__ == '__main__':
    main()
