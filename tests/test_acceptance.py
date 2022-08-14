import datetime
import os.path
import unittest
import tempfile
from typing import Union, ClassVar
import warnings

from faker import Faker
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import DATE as SQLITE_DATE
from sqlalchemy import create_engine

from faker_sqlalchemy import SqlAlchemyProvider
from tests.test_models import Base, Model, RelationshipModel, TypeOverrideModel


class _TestSessionFixture:
    def __init__(self, path=None):
        self._session = None
        self._temp_file = None

        if path is None:
            self._temp_file = tempfile.TemporaryDirectory()
            self._temp_file.__enter__()
            fs_path = os.path.join(self._temp_file.name, "db.sqlite3")
            path = f"sqlite:///{fs_path}"

        try:
            self.engine = create_engine(path, echo=False, future=True)
            self.Session = sessionmaker(bind=self.engine, future=True)
        except TypeError:
            # SA 1.3
            self.engine = create_engine(path, echo=False)
            self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def __enter__(self):
        self._session = self.Session()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            self._session.commit()
            self._session.close()

    def clear(self):
        with self as session:
            for m in Base.__subclasses__():
                session.query(m).delete()

    def teardown(self):
        Base.metadata.drop_all(self.engine)
        if self._temp_file:
            self._temp_file.__exit__(None, None, None)


class AcceptanceTests(unittest.TestCase):
    session_fixture: ClassVar[_TestSessionFixture]

    @classmethod
    def setUpClass(cls) -> None:
        cls._ctx = warnings.catch_warnings()
        cls._ctx.__enter__()
        warnings.simplefilter("ignore", category=SAWarning)

        cls.session_fixture = _TestSessionFixture(None)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls.session_fixture.teardown()

        cls._ctx.__exit__()

    def setUp(self) -> None:
        SqlAlchemyProvider.reset_type_mappings()

        super().setUp()

        self.session_fixture.clear()

        self.faker: Union[SqlAlchemyProvider, Faker] = Faker()
        self.faker.add_provider(SqlAlchemyProvider)

    def test_generates_models_for_model(self):
        model = self.faker.sqlalchemy_model(Model)
        self.assertIsInstance(model.big_integer, int)
        self.assertIsInstance(model.boolean, bool)
        self.assertIsInstance(model.date, datetime.date)
        self.assertIsInstance(model.datetime, datetime.datetime)
        self.assertIsInstance(model.float, float)
        self.assertIsInstance(model.integer, int)
        self.assertIsInstance(model.interval, datetime.timedelta)
        self.assertIsInstance(model.json, dict)
        self.assertIsInstance(model.large_binary, bytes)
        self.assertIsInstance(model.numeric, float)
        self.assertIsInstance(model.small_integer, int)
        self.assertIsInstance(model.string, str)
        self.assertIsInstance(model.time, datetime.time)
        self.assertIsInstance(model.unicode, str)
        self.assertIsInstance(model.unicode_text, str)

    def test_models_can_be_saved(self):
        model = self.faker.sqlalchemy_model(Model)

        with self.session_fixture as session:
            session.add_all([model])

            results = session.query(Model).first()

            self.assertEqual(results.unicode, model.unicode)

    def test_related_models_can_be_saved(self):
        model = self.faker.sqlalchemy_model(RelationshipModel, generate_related=True)

        with self.session_fixture as session:
            session.add_all([model, model.model])
            session.commit()

            results = session.query(RelationshipModel).first()

            self.assertIsNotNone(results.model.id)
            self.assertEqual(results.model.id, model.model_id)

    def test_types_can_be_registered(self):
        date = self.faker.date_time().date()

        def generate_sqlite_date(generator, column):
            return date

        SqlAlchemyProvider.register_type_mapping(
            SQLITE_DATE,
            generate_sqlite_date,
        )

        result = self.faker.sqlalchemy_model(TypeOverrideModel)
        self.assertEqual(result.sqlite_date, date)
