import pytest

from english_dictionary.database import DATABASE_DIRECTORY, DATABASE_NAME, Database
from pathlib import Path
from english_dictionary.api import BaseAPIBuilder
from .test_api import hello


@pytest.fixture
def database_dir():
    return Path(__file__).resolve().parent.parent / "english_dictionary"


def test_default_database_path(database_dir):
    assert DATABASE_DIRECTORY == database_dir

    assert DATABASE_DIRECTORY / DATABASE_NAME == database_dir / "words.db"


def test_database(hello):
    assert Database(":memory:") != Database(":memory:")
    a = Database(":memory:")
    a.save_word(BaseAPIBuilder.from_free_dictionary_api(hello))
    for row in a.fetch_all_words():
        assert row == BaseAPIBuilder.from_free_dictionary_api(hello)

    a.delete_word("hello")
    for row in a.fetch_all_words():
        assert row is None
