import json
import os

from settings import BASEDIR
from english_dictionary.utils.types import (
    WordData,
    Definition,
    RelatedWord,
    Pronunciation,
)

with open(os.path.join(BASEDIR, "try.json")) as f:
    json_data = json.load(f)

try_ = WordData.from_dict({"name": "try", "data": json_data})

test = WordData(
    name="test",
    etymology="From Middle English test, teste, from Old French test, teste (\u201can earthen vessel, especially a "
    "pot in which metals were tried\u201d), from Latin testum (\u201cthe lid of an earthen vessel, an "
    "earthen vessel, an earthen pot\u201d), from *terstus, past participle of the root *tersa "
    "(\u201cdry land\u201d). See terra, thirst",
    pronunciations=[
        Pronunciation(
            text=[
                "IPA: /t\u025bst/",
                "Rhymes: -\u025bst",
                "(South African) IPA: /test/",
            ]
        ),
    ],
    definitions=[
        Definition(
            part_of_speech="noun",
            texts=(
                "test (plural tests)",
                "A challenge, trial.",
                "A cupel or cupelling hearth in which precious metals are melted for trial and refinement.",
                "(academia) An examination, given often during the academic term.",
                "A session in which a product or piece of equipment is examined under everyday or extreme conditions to evaluate its durability, etc.",
                "(cricket, normally \u201cTest\u201d) A Test match.",
                "(marine biology) The external calciferous shell, or endoskeleton, of an echinoderm, e.g. sand dollars and sea urchins.",
                "(botany) Testa; seed coat.",
                "(obsolete) Judgment; distinction; discrimination.",
            ),
            related_words=(
                RelatedWord(
                    relationship_type="synonyms",
                    words=[
                        "(challenge, trial): See Thesaurus:test",
                        "(academics: examination): examination, quiz",
                    ],
                ),
                RelatedWord(
                    relationship_type="antonyms",
                    words=[
                        "(academics: examination): recess",
                    ],
                ),
            ),
            example_uses=[
                "Numerous experimental tests and other observations have been offered in favor of animal mind reading,"
                "and although many scientists are skeptical, others assert that humans are not the only species capable"
                "of representing what others do and don\u2019t perceive and know.",
                "Who would excel, when few can make a test / Betwixt indifferent writing and the best?",
            ],
        ),
        Definition(
            part_of_speech="verb",
            texts=(
                "test (third-person singular simple present tests, present participle testing, simple past and past participle tested)",
                "To challenge.",
                "To refine (gold, silver, etc.) in a test or cupel; to subject to cupellation.",
                "To put to the proof; to prove the truth, genuineness, or quality of by experiment, or by some principle or standard; to try.",
                "(academics) To administer or assign an examination, often given during the academic term, to (somebody).",
                "To place a product or piece of equipment under everyday and/or extreme conditions and examine it for its durability, etc.",
                "(copulative) To be shown to be by test.",
                "(chemistry) To examine or try, as by the use of some reagent.",
            ),
            example_uses=[
                "Climbing the mountain tested our stamina.",
                "to test the soundness of a principle; to test the validity of an argument",
                "Experience is the surest standard by which to test the real tendency of the existing constitution.",
                "Similar studies of rats have employed four different intracranial resorbable, slow sustained release systems\u2014\u00a0[\u2026]. Such a slow-release device containing angiogenic factors could be placed on the pia mater covering the cerebral cortex and tested in persons with senile dementia in long term studies.",
                "He tested positive for cancer.",
                "It is probable that children who test above 180 IQ are actually present in our juvenile population in greater frequency than at the rate of one in a million.",
                "to test a solution by litmus paper",
            ],
            related_words=(
                RelatedWord(
                    relationship_type="related term",
                    words=["attest", "contest", "detest", "protest"],
                ),
            ),
        ),
    ],
)
