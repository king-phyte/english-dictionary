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
        formatter_instance.parse_pronunciations() == "<p><b>Pronunciations:</b> kɪŋ</p>"
    )


# def test_parse_meanings(formatter_instance):
#     assert (
#         formatter_instance.parse_meanings().strip()
#         == "<b>Part of speech:</b> noun\n\n \n\n the male ruler of an independent state, especially one who "
#         "inherits the \n position by right of birth.\n\n \n\n <b>Example:</b> King Henry VIII\n\n \n\n "
#         "<b>Synonyms</b>: ruler, sovereign, monarch, supreme ruler, crowned head, \n majesty, Crown, "
#         "head of state, royal personage, emperor, prince, potentate, \n overlord, liege lord, lord, leader, "
#         "chief\n\n the most important chess piece, of which each player has one, which the \n opponent has to "
#         "checkmate in order to win. The king can move in any \n direction, including diagonally, to any adjacent "
#         "square that is not attacked \n by an opponent's piece or pawn.<hr /><b>Part of speech:</b> verb\n\n \n\n "
#         "make (someone) king.\n\n act in an unpleasantly superior and domineering way.\n\n \n\n <b>Example:</b> "
#         "he'll start kinging it over the lot of us again ".strip()
#     )
