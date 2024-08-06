from datetime import datetime, timezone
from app.models import User, Post, Category
from faker import Faker
import re

fake = Faker()

def seed_db(db):
    user1 = User(
        first_name='Nemanja',
        last_name='Petrovic',
        username='nemanja123',
        email='nemanja@gmail.com',
        birth_date=datetime.strptime('2000-01-19', '%Y-%m-%d').date(),
        role='Admin'
    )
    user1.set_password('123456');
    
    user2 = User(
        first_name='Mirko',
        last_name='Mirkovic',
        username='mirko123',
        email='mirko@gmail.com',
        birth_date=datetime.strptime('1989-11-10', '%Y-%m-%d').date(),
        role='Author'
    )
    user2.set_password('123456');

    user3 = User(
        first_name='Ana',
        last_name='Ivanovic',
        username='ana123',
        email='ana@gmail.com',
        birth_date=datetime.strptime('1999-02-07', '%Y-%m-%d').date(),
        role='Reader'
    )
    user3.set_password('123456')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    category1 = Category(name='Bussiness')
    category2 = Category(name='Sport')
    category3 = Category(name='Tech')
    category4 = Category(name='Nature')

    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.add(category4)
    db.session.commit()


    post1 = Post(
            title=re.sub(r'\.$','', fake.sentence()),
            body=generate_long_text(1000),
            author=user1,
            categories=[category1,category2],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    
    post2 = Post(
            title=re.sub(r'\.$','', fake.sentence()),
            body=generate_long_text(1000),
            author=user2,
            categories=[category2],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
    
    post3 = Post(
            title=re.sub(r'\.$','', fake.sentence()),
            body=generate_long_text(1000),
            author=user2,
            categories=[category3],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.commit()

def generate_long_text(min_chars):
    while True:
        text = fake.paragraph(nb_sentences=30, variable_nb_sentences=True)
        if len(text) >= min_chars:
            return text