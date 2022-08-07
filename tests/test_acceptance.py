import datetime
import unittest
from typing import Union
import warnings

from faker import Faker
from sqlalchemy.exc import SAWarning
from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import DATE as SQLITE_DATE
from sqlalchemy import (
    create_engine,
    select,
)

from faker_sqlalchemy import SqlAlchemyProvider
from tests.test_models import Base, Model, RelationshipModel, TypeOverrideModel

engine = create_engine("sqlite:///.test-db.sqlite3", echo=False, future=True)


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._ctx = warnings.catch_warnings()
        cls._ctx.__enter__()
        warnings.simplefilter("ignore", category=SAWarning)

        Base.metadata.create_all(engine)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        Base.metadata.drop_all(engine)
        cls._ctx.__exit__()

    def setUp(self) -> None:
        SqlAlchemyProvider.reset_type_mappings()

        super().setUp()

        with Session(engine) as session:
            for m in Base.__subclasses__():
                session.query(m).delete()
            session.commit()

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

        with Session(engine) as session:
            session.add_all([model])
            session.commit()

            results = session.scalars(
                select(Model)
            ).one()
            self.assertEqual(results.unicode, model.unicode)

    def test_related_models_can_be_saved(self):
        model = self.faker.sqlalchemy_model(RelationshipModel, generate_related=True)

        with Session(engine) as session:
            session.add_all([model])
            session.commit()

            results = session.scalars(
                select(RelationshipModel),
            ).one()
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
