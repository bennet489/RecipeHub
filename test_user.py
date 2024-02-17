import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_hashing(self):
        user = User(username='lizzy', email='lizzy@gmail.com')
        user.set_password('iamlizzy')
        self.assertFalse(user.check_password('mypass'))
        self.assertTrue(user.check_password('iamlizzy'))

    def text_avatar(self):
        user = User(username='lizzy', email='lizzy@gmail.com')
        self.assertEqual(user.avatar(128), ('https://www.gravatar.com/avatar/'
                                            'd4c74594d841139328695756648b6bd6'
                                            '?d=identicon&s=128'))
    
    def test_follow(self):
        user1 = User(username='lizzy', email='lizzy@gmail.com')
        user2 = User(username='john', email='john@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        following = db.session.scalars(user1.following.select()).all()
        follower = db.session.scalars(user2.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(follower, [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 1)
        self.assertEqual(user2.followers_count(), 1)
        user1_following = db.session.scalars(user1.following.select()).all()
        user2_followers = db.session.scalars(user2.followers.select()).all()
        self.assertEqual(user1_following[0].username, 'john')
        self.assertEqual(user2_followers[0].username, 'lizzy')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 0)
        self.assertEqual(user2.followers_count(), 0)


    def test_follow_post(self):
        user1 = User(username='lizzy', email='lizzy@gmail.com')
        user2 = User(username='john', email='john@gmail.com')
        user3 = User(username='joe', email='joe@gmail.com')
        user4 = User(username='kate', email='kate@gmail.com')
        db.session.add_all([user1, user2, user3, user4])

        now = datetime.now(timezone.utc)
        post1 = Post(body="How to make pizza",
                     author=user1, timestamp=now + timedelta(seconds=1))
        post2 = Post(body='How to make smoky jellof rice',
                     author=user2, timestamp=now + timedelta(seconds=4))
        post3 = Post(body='Kontomire stew recipe',
                     author=user3, timestamp=now + timedelta(seconds=2))
        post4 = Post(body='Coconut rice recipe...',
                     author=user4, timestamp=now + timedelta(seconds=3))
        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()

        user1.follow(user2)
        user1.follow(user4)
        user2.follow(user3)
        user3.follow(user4)
        db.session.commit()

        f1 = db.session.scalars(user1.following_posts()).all()
        f2 = db.session.scalars(user2.following_posts()).all()
        f3 = db.session.scalars(user3.following_posts()).all()
        f4 = db.session.scalars(user4.following_posts()).all()
        self.assertEqual(f1, [post2, post4, post1])
        self.assertEqual(f2, [post2, post3])
        self.assertEqual(f3, [post4, post3])
        self.assertEqual(f4, [post4])
    

if __name__ == '__main__':
    unittest.main(verbosity=2)
