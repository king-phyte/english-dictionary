from typing import Sequence
import requests


class BaseAPIBuilder:
    """
    Desired final API
    {
        "name": str,
        "etymology": str,
        "pronunciations: [
            {
                "text": str,
                "audio": str,
            }
        ]
        "meanings": [
            {
                "part_of_speech": str,
                "definitions": [
                    {
                        "definition": str,
                        "example": str,
                        "related_words": [
                            {
                                "relationship_type": str,
                                "words": list[str],
                            },
                        ]
                    }
                ]
            }
        ]
    }
    """

    @staticmethod
    def from_free_dictionary_api(api: Sequence[dict]):
        return [
            {
                "name": data_group.get("word"),
                "pronunciations": data_group.get("phonetics"),
                "etymology": data_group.get("origin"),
                "meanings": [
                    {
                        "part_of_speech": meaning.get("partOfSpeech"),
                        "definitions": [
                            {
                                "definition": definition.get("definition"),
                                "example": definition.get("example"),
                                "related_words": [
                                    {
                                        "relationship_type": "synonyms",
                                        "words": definition.get("synonyms"),
                                    },
                                    {
                                        "relationship_type": "antonyms",
                                        "words": definition.get("antonyms"),
                                    },
                                ],
                            }
                            for definition in meaning.get("definitions")
                        ],
                    }
                    for meaning in data_group.get("meanings")
                ],
            }
            for data_group in api
        ]


class FreeDictionaryApi:
    BASE_URL = r"https://api.dictionaryapi.dev/api/v2/entries/en/"

    def __init__(self):
        self._word = None

    def get_word_data(self, word: str):
        self._word = requests.get(FreeDictionaryApi.BASE_URL + word.lower())

        if self._word.status_code == 200:
            return self._word

        self._word.raise_for_status()

    def get_json(self, word: str):
        return self.get_word_data(word).json()
