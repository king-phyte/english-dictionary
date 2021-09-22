import requests


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
