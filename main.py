from PyQt5.QtWidgets import QApplication

from gui.components import MainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

    # parser = WiktionaryParser()
    # word = parser.fetch("dictionary")
    #
    # with open("./another.json", "w") as f:
    #     json.dump(word, f, indent=4)
#     another_word = parser.fetch("test", "french")
#     parser.set_default_language("french")
#     parser.exclude_part_of_speech("noun")
#     parser.include_relation("alternative forms")
#
#     test = HumanReadableFormat(word)
#     test.display()
#     another_word = HumanReadableFormat(another_word)
#     another_word.display()
#     begging = parser.fetch("begging")
#     begging = HumanReadableFormat(begging)
#     begging.display()
#
# from utils.types import Dictionary
#
#
# if __name__ == "__main__":
#     test = {
#         "test": [
#             {
#                 "etymology": "From Middle English test, teste, from Old French test, teste (\u201can earthen vessel, especially a pot in which metals were tried\u201d), from Latin testum (\u201cthe lid of an earthen vessel, an earthen vessel, an earthen pot\u201d), from *terstus, past participle of the root *tersa (\u201cdry land\u201d). See terra, thirst.\n",
#                 "definitions": [
#                     {
#                         "part_of_speech": "noun",
#                         "text": [
#                             "test (plural tests)",
#                             "A challenge, trial.",
#                             "A cupel or cupelling hearth in which precious metals are melted for trial and refinement.",
#                             "(academia) An examination, given often during the academic term.",
#                             "A session in which a product or piece of equipment is examined under everyday or extreme conditions to evaluate its durability, etc.",
#                             "(cricket, normally \u201cTest\u201d) A Test match.",
#                             "(marine biology) The external calciferous shell, or endoskeleton, of an echinoderm, e.g. sand dollars and sea urchins.",
#                             "(botany) Testa; seed coat.",
#                             "(obsolete) Judgment; distinction; discrimination.",
#                         ],
#                         "related_words": [
#                             {
#                                 "relationship_type": "synonyms",
#                                 "words": [
#                                     "(challenge, trial): See Thesaurus:test",
#                                     "(academics: examination): examination, quiz",
#                                 ],
#                             },
#                             {
#                                 "relationship_type": "antonyms",
#                                 "words": ["(academics: examination): recess"],
#                             },
#                             {
#                                 "relationship_type": "hyponyms",
#                                 "words": [
#                                     "acid test",
#                                     "babysitter test",
#                                     "blood test",
#                                     "duck test",
#                                     "field test",
#                                     "flame test",
#                                     "inkblot test",
#                                     "litmus test",
#                                     "multiple-choice test",
#                                     "nose test",
#                                     "Rorschach test",
#                                     "single-choice test",
#                                     "smell test",
#                                     "smoke test",
#                                     "sniff test",
#                                     "software test",
#                                     "stress test",
#                                 ],
#                             },
#                         ],
#                         "example_uses": [
#                             "Numerous experimental tests and other observations have been offered in favor of animal mind reading, and although many scientists are skeptical, others assert that humans are not the only species capable of representing what others do and don\u2019t perceive and know.",
#                             "Who would excel, when few can make a test / Betwixt indifferent writing and the best?",
#                         ],
#                     },
#                     {
#                         "part_of_speech": "verb",
#                         "text": [
#                             "test (third-person singular simple present tests, present participle testing, simple past and past participle tested)",
#                             "To challenge.",
#                             "To refine (gold, silver, etc.) in a test or cupel; to subject to cupellation.",
#                             "To put to the proof; to prove the truth, genuineness, or quality of by experiment, or by some principle or standard; to try.",
#                             "(academics) To administer or assign an examination, often given during the academic term, to (somebody).",
#                             "To place a product or piece of equipment under everyday and/or extreme conditions and examine it for its durability, etc.",
#                             "(copulative) To be shown to be by test.",
#                             "(chemistry) To examine or try, as by the use of some reagent.",
#                         ],
#                         "related_words": [],
#                         "example_uses": [
#                             "Climbing the mountain tested our stamina.",
#                             "to test the soundness of a principle; to test the validity of an argument",
#                             "Experience is the surest standard by which to test the real tendency of the existing constitution.",
#                             "Similar studies of rats have employed four different intracranial resorbable, slow sustained release systems\u2014\u00a0[\u2026]. Such a slow-release device containing angiogenic factors could be placed on the pia mater covering the cerebral cortex and tested in persons with senile dementia in long term studies.",
#                             "He tested positive for cancer.",
#                             "It is probable that children who test above 180 IQ are actually present in our juvenile population in greater frequency than at the rate of one in a million.",
#                             "to test a solution by litmus paper",
#                         ],
#                     },
#                 ],
#                 "pronunciations": {
#                     "text": [
#                         "IPA: /t\u025bst/",
#                         "Rhymes: -\u025bst",
#                         "(South African) IPA: /test/",
#                     ],
#                     "audio": [
#                         "//upload.wikimedia.org/wikipedia/commons/9/9c/En-us-test.ogg",
#                         "//upload.wikimedia.org/wikipedia/commons/d/d5/En-uk-a_test.ogg",
#                     ],
#                 },
#             },
#             {
#                 "etymology": "From Middle English teste, from Old French teste, test and Latin testis (\u201cone who attests, a witness\u201d).\n",
#                 "definitions": [
#                     {
#                         "part_of_speech": "noun",
#                         "text": ["test (plural tests)", "(obsolete) A witness."],
#                         "related_words": [],
#                         "example_uses": [
#                             "Prelates and great lords of England, who were for the more surety tests of that deed."
#                         ],
#                     },
#                     {
#                         "part_of_speech": "verb",
#                         "text": [
#                             "test (third-person singular simple present tests, present participle testing, simple past and past participle tested)",
#                             "(obsolete, transitive) To attest (a document) legally, and date it.",
#                             "(obsolete, intransitive) To make a testament, or will.",
#                         ],
#                         "related_words": [
#                             {
#                                 "relationship_type": "related terms",
#                                 "words": ["attest", "contest", "detest", "protest"],
#                             }
#                         ],
#                         "example_uses": [],
#                     },
#                 ],
#                 "pronunciations": {
#                     "text": [
#                         "IPA: /t\u025bst/",
#                         "Rhymes: -\u025bst",
#                         "(South African) IPA: /test/",
#                     ],
#                     "audio": [
#                         "//upload.wikimedia.org/wikipedia/commons/9/9c/En-us-test.ogg",
#                         "//upload.wikimedia.org/wikipedia/commons/d/d5/En-uk-a_test.ogg",
#                     ],
#                 },
#             },
#             {
#                 "etymology": "Clipping of testosterone.\n",
#                 "definitions": [
#                     {
#                         "part_of_speech": "noun",
#                         "text": [
#                             "test (uncountable)",
#                             "(informal, slang, body building) testosterone",
#                         ],
#                         "related_words": [],
#                         "example_uses": [],
#                     }
#                 ],
#                 "pronunciations": {
#                     "text": [
#                         "IPA: /t\u025bst/",
#                         "Rhymes: -\u025bst",
#                         "(South African) IPA: /test/",
#                     ],
#                     "audio": [
#                         "//upload.wikimedia.org/wikipedia/commons/9/9c/En-us-test.ogg",
#                         "//upload.wikimedia.org/wikipedia/commons/d/d5/En-uk-a_test.ogg",
#                     ],
#                 },
#             },
#         ],
#     }
#
#     my_dictionary = Dictionary()
#
#     my_dictionary.add_word({"king": "Something something"})
#     my_dictionary.add_word({"mine": "Something something"})
#     my_dictionary.add_word({"go": "Something something"})
#     my_dictionary.add_word({"huh": "Something something"})
#     my_dictionary.add_word({"rbac": "Something something"})
#     my_dictionary.add_word({"aing": "Something something"})
#
#     # my_dictionary.add_word(test)
#     # my_dictionary.find_word("test")
#     # my_dictionary.display("test")
#     # my_dictionary.add_word("prof")
#     print(my_dictionary)
