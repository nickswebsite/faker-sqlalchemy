"""`SQLAlchemy Faker <https://faker-sqlalchemy.readthedocs.io/en/latest/>`_ is a provider for the
`Faker <https://github.com/joke2k/faker>`_ library that helps populate `SQLAlchemh ORM <https://www.sqlalchemy.org/>`_
models with dummy data. Creating a new instance of a model can be as simple as calling
``fake.sqlalchemy_model(SomeModel)``.


Installation
------------

The recommend way to install SQLAlchemy Faker is with ``pip``::

    pip install faker_sqlalchemy

Example
-------

Say you have some model declared using SQLAlchemy's ORM.

>>> class SomeModel(Base):
...     __tablename__ = "some_model"
...
...     id = Column(Integer, primary_key=True)
...
...     value = Column(String)

And, you want to easily generate some data,

>>> from faker_sqlalchemy import SqlAlchemyProvider
>>>
>>> fake = Faker()
>>> fake.add_provider(SqlAlchemyProvider)
>>>
>>> instance = fake.sqlalchemy_model(SomeModel)

Use ``instance`` as desired.

>>> print(instance.value)
RNvnAvOpyEVAoNGnVZQU
"""

import datetime
from typing import Any, TypeVar, Type, Dict, Union, List, Callable

from faker import Faker
from faker.providers import BaseProvider
from faker.providers.date_time import Provider as DateTimeProvider
from faker.providers.misc import Provider as MiscProvider
from faker.providers.python import Provider as PythonProvider
from sqlalchemy.orm import DeclarativeMeta, Mapper, RelationshipProperty
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy import (
    inspect,
    Column,
    ARRAY,
    BIGINT,
    BigInteger,
    BINARY,
    BLOB,
    BOOLEAN,
    Boolean,
    CHAR,
    CLOB,
    DATE,
    Date,
    DATETIME,
    DateTime,
    DECIMAL,
    Enum,
    FLOAT,
    Float,
    INT,
    INTEGER,
    Integer,
    Interval,
    JSON,
    LargeBinary,
    NCHAR,
    NUMERIC,
    Numeric,
    NVARCHAR,
    PickleType,
    REAL,
    SMALLINT,
    SmallInteger,
    String,
    TEXT,
    TIME,
    Time,
    TIMESTAMP,
    TupleType,
    TypeDecorator,
    Unicode,
    UnicodeText,
    VARBINARY,
    VARCHAR,
)

__version__ = "0.10.220807"
__all__ = (
    "SqlAlchemyProvider",
)

ModelType = TypeVar("ModelType")
ColumnType = TypeVar("ColumnType", bound=TypeEngine)
PrimitiveJsonTypes = Union[str, int, bool, None]
GeneratorFunction = Callable[
    [Faker, Column], Column
]
GeneratorSpec = Union[str, GeneratorFunction]


def _generate_date(generator: DateTimeProvider, _: Any) -> datetime.date:
    return generator.date_time().date()


def _generate_time(generator: DateTimeProvider, _: Any) -> datetime.time:
    return generator.date_time().time()


def _generate_json(generator: PythonProvider, _: Any) -> Dict[str, Union[str, int, bool, List[PrimitiveJsonTypes], Dict[str, PrimitiveJsonTypes]]]:
    return generator.pydict(
        10,
        True,
        [
            str,
            int,
            bool,
        ],
    )


def _generate_small_bytes(generator: MiscProvider, _: Any) -> bytes:
    return generator.binary(100)


DEFAULT_MAPPINGS: Dict[TypeEngine, GeneratorSpec] = {
    BigInteger: "pyint",
    Boolean: "pybool",
    Date: _generate_date,
    DateTime: "date_time",
    Float: "pyfloat",
    Integer: "pyint",
    Interval: "time_delta",
    JSON: _generate_json,
    LargeBinary: "binary",
    Numeric: "pyfloat",
    SmallInteger: "pyint",
    String: "pystr",
    # Text: "pystr",
    Time: _generate_time,
    Unicode: "pystr",
    UnicodeText: "pystr",
}


class SqlAlchemyProvider(BaseProvider):
    """Generates instances of models declared with SQLAlchemy's ORM's declarative_base.

    Model instances are generated based on their column types. Generators for custom
    column types may be registered with :meth:`register_type_mapping()`.

    Methods:

    * :meth:`sqlalchemy_model`: Generates an instance of the given model.
    * :meth:`register_type_mapping`: Tell providers which generator to use
      for ``type``.
    """
    MAPPINGS = DEFAULT_MAPPINGS.copy()

    generator: BaseProvider

    @classmethod
    def register_type_mapping(cls, type: TypeEngine, spec: GeneratorSpec):
        """Registers `spec` as a generator for columns of the given `type`.

        `spec` may be:

        (1) a string indicating a method on the faker that may be
            called without arguments, or
        (2) A callable that accepts a faker generator and a SQLAlchemy callable.

        Column types are looked up by exact match first, then base classes are
        searched using `isinstance`.

        :param type: The column type that `spec` should apply to.
        :param spec: The generator spec indicating how to generate the object.
        """
        cls.MAPPINGS[type] = spec

    @classmethod
    def reset_type_mappings(cls):
        """Resets type mappings back to defaults."""
        cls.MAPPING = DEFAULT_MAPPINGS.copy()

    def sqlalchemy_model(
            self, model: Type[ModelType], generate_primary_keys=False, generate_related=False, **overrides
    ) -> ModelType:
        """Create an instance of ``model`` based on its column specification.

        The columns of ``model`` are introspected to determine how their values are to be
        constructed. Neither primary keys, nor related models are generated by default.
        To generate the primary keys for the model, set ``primary_keys`` to ``True``. To
        generate related models defined by ``relationship``, set ``generate_related`` to
        ``True``.

        Currently, ``primary_keys`` and ``generate_related`` are mutually exclusive, so
        primary keys will NOT be generated from related models. If this functionality
        is desired, then the keys will need to be reconciled manually.

        :param model: The model to create an instance of.
        :param generate_related: Generate relationship models.
        :param generate_primary_keys: Generate primary key fields.
        :param overrides: Predetermined values to attach to the generated instance.
        :return: Returns a new instance of ``model``.
        """
        assert isinstance(model, DeclarativeMeta)
        assert not (generate_primary_keys and generate_related), "`generate_primary_keys` and `generate_related` " \
                                                                 "MUST NOT both be set to True"

        inspection: Mapper = inspect(model)

        values = {}
        for column in inspection.columns:
            if column.name in overrides:
                values[column.name] = overrides[column.name]
            elif not column.primary_key or generate_primary_keys:
                if not column.foreign_keys:
                    values[column.name] = self.sqlalchemy_column_value(column)

        if generate_related:
            relationship_property: RelationshipProperty
            for key, relationship_property in inspection.relationships.items():
                values[key] = self.sqlalchemy_model(
                    relationship_property.mapper.class_, generate_primary_keys=generate_primary_keys, generate_related=True
                )

        return model(**values)

    def sqlalchemy_column_value(self, column: Column) -> ColumnType:
        """Creates an instance of a type specified by ``column``.

        :param column: A SQLAlchemy ``Column``
        :return: Returns a value that may be assigned to ``Column`` attributes.
        """

        generator_spec = self._find_generator_spec(column)

        if callable(generator_spec):
            return generator_spec(self.generator, column)
        else:
            return self._find_generator(generator_spec)()

    def _find_generator_spec(self, column: Column):
        if type(column.type) in self.MAPPINGS:
            return self.MAPPINGS[type(column.type)]
        else:
            for k, v in self.MAPPINGS.items():
                if isinstance(column.type, k):
                    return v
        raise ValueError(f"Unmapped column type found for column: {column}")

    def _find_generator(self, generator_spec):
        if hasattr(self.generator, generator_spec):
            return getattr(self.generator, generator_spec)
        else:
            return getattr(self, generator_spec)
