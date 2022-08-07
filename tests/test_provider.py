import unittest
from typing import Union

from faker import Faker

from faker_sqlalchemy import SqlAlchemyProvider
from tests.test_models import Model, RelationshipModel


class SqlAlchemyProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        SqlAlchemyProvider.reset_type_mappings()

        super().setUp()

        self.faker: Union[SqlAlchemyProvider, Faker] = Faker()
        self.faker.add_provider(SqlAlchemyProvider)

    def test_primary_key_fields_are_not_generated_by_default(self):
        result = self.faker.sqlalchemy_model(Model)
        self.assertIsNone(result.id)

    def test_primary_key_fields_may_be_generated(self):
        result = self.faker.sqlalchemy_model(Model, generate_primary_keys=True)
        self.assertIsNotNone(result.id)

    def test_fields_may_be_overridden(self):
        override = self.faker.pystr()
        result = self.faker.sqlalchemy_model(Model, string=override)
        self.assertEqual(result.string, override)

    def test_relationships_are_set_to_none_by_default(self):
        result = self.faker.sqlalchemy_model(RelationshipModel)
        self.assertIsNone(result.model_id)
        self.assertIsNone(result.model)

    def test_related_models_may_be_generated(self):
        result = self.faker.sqlalchemy_model(RelationshipModel, generate_related=True)
        self.assertIsNotNone(result.model)
        self.assertIsNone(result.model_id)

    @unittest.skip("Not Implemented")
    def test_related_models_have_primary_keys_generated(self):
        result = self.faker.sqlalchemy_model(RelationshipModel, generate_related=True, generate_primary_keys=True)
        self.assertIsNotNone(result.model_id)
        self.assertEqual(result.model_id, result.model.id)
