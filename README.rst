Fakers for SQLAlchemy
=====================

[![PyPI](https://img.shields.io/pypi/v/faker_sqlalchemy)](https://pypi.org/project/faker_sqlalchemy/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/faker_sqlalchemy.svg)](https://pypi.org/project/faker_sqlalchemy/)
[![Documentation](https://readthedocs.org/projects/faker-sqlalchemy/badge/?version=latest)](https://faker-sqlalchemy.readthedocs.io/en/latest/?badge=latest)

`SQLAlchemy Faker <https://faker-sqlalchemy.readthedocs.io/en/latest/>`_ is a provider for the
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
