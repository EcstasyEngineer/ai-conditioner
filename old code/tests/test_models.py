# tests/test_models.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from old.database.models import Base, User, Line
from old.database.database import get_session

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use an in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    def test_user_creation(self):
        new_user = User(
            preferred_dominant='Master',
            subject_name='Slave',
            subject_gender='F',
            dominant_gender='M'
        )
        self.session.add(new_user)
        self.session.commit()
        user = self.session.query(User).first()
        self.assertEqual(user.preferred_dominant, 'Master')
        self.assertEqual(user.subject_name, 'Slave')

    def test_line_creation(self):
        new_line = Line(
            template_id=1,
            real_text='I obey Master.',
            subject='Slave',
            sub_gender='F',
            sub_pov='1PS',
            dominant='Master',
            dom_gender='M',
            dom_pov='2PS'
        )
        self.session.add(new_line)
        self.session.commit()
        line = self.session.query(Line).first()
        self.assertEqual(line.real_text, 'I obey Master.')
        self.assertEqual(line.sub_pov, '1PS')

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.engine.dispose()

if __name__ == '__main__':
    unittest.main()
