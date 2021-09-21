from typing import List, Dict, Optional


class Definition(object):
    def __init__(
        self,
        part_of_speech=None,
        text=None,
        related_words=None,
        example_uses=None,
        *args,
        **kwargs,
    ) -> None:
        self.part_of_speech = part_of_speech if part_of_speech else ""
        self.texts = text if text else ""
        self.related_words = related_words if related_words else []
        self.example_uses = example_uses if example_uses else []

    @property
    def related_words(self):
        return self._related_words

    @related_words.setter
    def related_words(self, related_words):
        if related_words is None:
            self._related_words = []
            return
        elif not isinstance(related_words, list):
            raise TypeError("Invalid type for relatedWord")
        else:
            # for element in related_words:
            #     if not isinstance(element, RelatedWord):
            #         raise TypeError("Invalid type for relatedWord")
            self._related_words = related_words

    def to_json(self):
        return {
            "part_of_speech": self.part_of_speech,
            "texts": self.texts,
            "related_words": [
                related_word.to_json() for related_word in self.related_words
            ],
            "example_uses": self.example_uses,
        }

    def __getitem__(self, item):
        return getattr(item)


class RelatedWord(object):
    def __init__(self, relationship_type=None, words=None, *args, **kwargs):
        self.relationship_type = relationship_type if relationship_type else ""
        self.words = words if words else []

    def to_json(self):
        return {"relationship_type": self.relationship_type, "words": self.words}

    def __getitem__(self, item):
        return getattr(item)


class Pronunciation:
    def __init__(
        self, text: List[str] = None, audio: List[str] = None, *args, **kwargs
    ) -> None:
        self.text = text if text is not None else []
        self.audio = audio if audio is not None else []

    def __getitem__(self, item):
        return getattr(item)


class WordData(object):
    def __init__(
        self,
        etymology: Optional[str] = None,
        definitions: Optional[List[Definition]] = None,
        pronunciations: Optional[Dict[str, List[str]]] = None,
        audio_links: Optional[List[str]] = None,
        *args,
        **kwargs,
    ):
        self.etymology = etymology if etymology else ""
        self.definition_list = definitions
        self.pronunciations = pronunciations if pronunciations else []
        self.audio_links = audio_links if audio_links else []

    @property
    def definition_list(self):
        return self._definition_list

    @definition_list.setter
    def definition_list(self, definitions):
        if definitions is None:
            self._definition_list = []
            return
        elif not isinstance(definitions, list):
            raise TypeError("Invalid type for definition")
        else:
            # for element in definitions:
            #     if not isinstance(element, Definition):
            #         raise TypeError("Invalid type for definition")
            self._definition_list = definitions

    def to_json(self):
        return {
            "etymology": self.etymology,
            "definitions": [
                definition.to_json() for definition in self._definition_list
            ],
            "pronunciations": {"text": self.pronunciations, "audio": self.audio_links},
        }

    def __getitem__(self, item):
        return getattr(item)
