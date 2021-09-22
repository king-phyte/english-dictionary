from english_dictionary.api import FreeDictionaryApi, BaseAPIBuilder


import pytest


@pytest.fixture
def king():
    return [
        {
            "word": "king",
            "phonetic": "kɪŋ",
            "phonetics": [
                {
                    "text": "kɪŋ",
                    "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/king--1_gb_1.mp3",
                }
            ],
            "origin": (
                "Old English cyning, cyng, of Germanic origin;"
                "related to Dutch koning and German König, also to kin."
            ),
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": (
                                "the male ruler of an independent state, especially one who inherits"
                                "the position by right of birth."
                            ),
                            "example": "King Henry VIII",
                            "synonyms": [
                                "ruler",
                                "sovereign",
                                "monarch",
                                "supreme ruler",
                                "crowned head",
                                "majesty",
                                "Crown",
                                "head of state",
                                "royal personage",
                                "emperor",
                                "prince",
                                "potentate",
                                "overlord",
                                "liege lord",
                                "lord",
                                "leader",
                                "chief",
                            ],
                            "antonyms": [],
                        },
                        {
                            "definition": (
                                "the most important chess piece, of which each player has one,"
                                "which the opponent has to checkmate in order to win."
                                "The king can move in any direction, including diagonally, to any"
                                "adjacent square that is not attacked by an opponent's piece or pawn."
                            ),
                            "synonyms": [],
                            "antonyms": [],
                        },
                    ],
                },
                {
                    "partOfSpeech": "verb",
                    "definitions": [
                        {
                            "definition": "make (someone) king.",
                            "synonyms": [],
                            "antonyms": [],
                        },
                        {
                            "definition": "act in an unpleasantly superior and domineering way.",
                            "example": "he'll start kinging it over the lot of us again",
                            "synonyms": [],
                            "antonyms": [],
                        },
                    ],
                },
            ],
        },
        {
            "word": "God Save the Queen",
            "phonetic": "ɡɒdseɪvðəˈkwiːn",
            "phonetics": [
                {
                    "text": "ɡɒdseɪvðəˈkwiːn",
                    "audio": "//ssl.gstatic.com/dictionary/static/sounds/20200429/god_save_the_queen--1_gb_1.mp3",
                }
            ],
            "origin": (
                "evidence suggests a 17th-century origin for the complete words and tune of the anthem."
                "The ultimate origin is obscure: the phrase ‘God save the King’ occurs in various passages in the"
                "Old Testament, while as early as 1545 it was a watchword in the navy, with ‘long to reign over us’"
                "as a countersign."
            ),
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": "the British national anthem.",
                            "synonyms": [],
                            "antonyms": [],
                        }
                    ],
                }
            ],
        },
    ]


@pytest.fixture
def hello():
    return [
        {
            "word": "hello",
            "phonetics": [
                {
                    "text": "/həˈloʊ/",
                    "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_1_rr.mp3",
                },
                {
                    "text": "/hɛˈloʊ/",
                    "audio": "https://lex-audio.useremarkable.com/mp3/hello_us_2_rr.mp3",
                },
            ],
            "meanings": [
                {
                    "partOfSpeech": "exclamation",
                    "definitions": [
                        {
                            "definition": "Used as a greeting or to begin a phone conversation.",
                            "example": "hello there, Katie!",
                        }
                    ],
                },
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": "An utterance of “hello”; a greeting.",
                            "example": "she was getting polite nods and hellos from people",
                            "synonyms": [
                                "greeting",
                                "welcome",
                                "salutation",
                                "saluting",
                                "hailing",
                                "address",
                                "hello",
                                "hallo",
                            ],
                        }
                    ],
                },
                {
                    "partOfSpeech": "intransitive verb",
                    "definitions": [
                        {
                            "definition": "Say or shout “hello”; greet someone.",
                            "example": "I pressed the phone button and helloed",
                        }
                    ],
                },
            ],
        }
    ]


@pytest.fixture
def free_dictionary_api_instance_with_word_king(mocker, king):
    instance = mocker.patch("english_dictionary.api.FreeDictionaryApi")
    instance.get_json.return_value = king
    return instance


@pytest.fixture
def free_dictionary_api_instance_with_word_hello(mocker, hello):
    instance = mocker.patch("english_dictionary.api.FreeDictionaryApi")
    instance.get_json.return_value = hello
    return instance


class TestFreeDictionaryAPI:
    def test_base_url(self):
        assert (
            FreeDictionaryApi.BASE_URL
            == r"https://api.dictionaryapi.dev/api/v2/entries/en/"
        )

    def test_word_king(self, free_dictionary_api_instance_with_word_king):
        king_data = free_dictionary_api_instance_with_word_king.get_json()

        assert len(king_data) == 2

        for section in ("word", "phonetics", "origin", "meanings"):
            assert section in king_data[0].keys()

    def test_word_hello(self, free_dictionary_api_instance_with_word_hello):
        hello_data = free_dictionary_api_instance_with_word_hello.get_json()
        assert len(hello_data) == 1


class TestBaseAPIBuilder:
    def test_get_desired_sections(self, king):
        converter = BaseAPIBuilder.from_free_dictionary_api(king)

        for i, section in enumerate(converter):
            assert section.get("name") == king[i].get("word")
            assert section.get("etymology") == king[i].get("origin")
            assert section.get("pronunciations") == king[i].get("phonetics")
            # assert section.get("meanings") == king[i].get("meanings")
