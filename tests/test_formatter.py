import pytest

from english_dictionary.utils.formatter import BaseAPIFormatter
from english_dictionary.api import BaseAPIBuilder
from english_dictionary.types import WordData

from .test_api import king


@pytest.fixture
def formatter_instance(king):
    word = BaseAPIBuilder.from_free_dictionary_api(king)
    return BaseAPIFormatter(WordData.from_api(word))


def test_parse_etymology(formatter_instance):
    assert formatter_instance.parse_etymology() == (
        "<b>Etymology:</b> Old English cyning, cyng, of Germanic origin;"
        "related to Dutch koning and German König, also to kin."
    )


def test_parse_pronunciations(formatter_instance):
    assert (
        formatter_instance.parse_pronunciations()
        == "<p><b>Pronunciations:</b></p> <p><b>kɪŋ</b></p>"
    )


def test_parse_meanings(formatter_instance):
    assert formatter_instance.parse_meanings() == ""
