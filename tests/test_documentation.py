import unittest
import doctest

from faker import Faker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import faker_sqlalchemy

Base = declarative_base()


def _doctest_faker():
    fake = Faker()
    fake.seed_instance(0)
    return fake


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(
        faker_sqlalchemy,
        {
            "Base": Base,
            "Faker": _doctest_faker,
            "Column": Column,
            "Integer": Integer,
            "String": String,
        }
    ))
    return tests
