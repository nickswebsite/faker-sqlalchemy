Fakers for SQLAlchemy
=====================

|PyPI| |Build| |Supported Python versions| |Documentation| |Downloads| 

`SQLAlchemy Faker <https://faker-sqlalchemy.readthedocs.io/en/latest/>`_ is a provider for the
`Faker <https://github.com/joke2k/faker>`_ library that helps populate `SQLAlchemy ORM <https://www.sqlalchemy.org/>`_
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

Supported Versions
------------------

Currently SQLAlchemy versions 1.3 and 1.4 are supported. Support for SQLAlchemy 2.0 will be added when it is released.

Faker versions ``>=8`` are currently supported, though it should be noted that the testing matrix isn't exhaustive. If
bugs come up with a particular version of faker beyond version 8.0, submit a ticket to add support.

Python versions ``>=3.7`` are currently supported. If python 3.6 support is desired, submit a ticket to add support. Support
for Python 3.11 will be added when it is officially supported by SQLAlchemy. Currently, this is waiting on greenlet
releasing support for python 3.11.


.. |PyPI| image:: https://img.shields.io/pypi/v/faker_sqlalchemy
   :target: https://pypi.org/project/faker_sqlalchemy/
.. |Build| image:: https://github.com/nickswebsite/faker-sqlalchemy/actions/workflows/package.yml/badge.svg
   :target: https://github.com/nickswebsite/faker-sqlalchemy/actions/workflows/package.yml
.. |Supported Python versions| image:: https://img.shields.io/pypi/pyversions/faker_sqlalchemy.svg
   :target: https://pypi.org/project/faker_sqlalchemy/
.. |Documentation| image:: https://readthedocs.org/projects/faker-sqlalchemy/badge/?version=latest
   :target: https://faker-sqlalchemy.readthedocs.io/en/latest/?badge=latest
.. |Downloads| image:: https://pepy.tech/badge/faker_sqlalchemy/month
   :target: https://pepy.tech/project/faker_sqlalchemy/
