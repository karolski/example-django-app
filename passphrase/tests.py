from unittest import TestCase

from passphrase.passphrase_validation import (
    contains_unique_anagrams,
    contains_unique_words,
    count_valid_passphrases_advanced,
    count_valid_passphrases_basic,
)


class TestPassphraseValidation(TestCase):
    def test_invalid_passphrase_basic(self):
        self.assertEquals(contains_unique_words("aa bb cc dd aa"), False)

    def test_valid_passphrase_basic(self):
        self.assertEquals(contains_unique_words("aa bb cc dd aaa"), True)

    def test_count_valid_passphrases_basic(self):
        count = count_valid_passphrases_basic(
            [
                "aa bb cc dd ee",
                "aa bb cc dd aa",
                "aa bb cc dd aaa",
            ]
        )
        self.assertEquals(count, 2)

    def test_invalid_passphrase_advanced(self):
        self.assertEquals(contains_unique_anagrams("abcde xyz ecdab"), False)

    def test_valid_passphrase_advanced(self):
        self.assertEquals(contains_unique_anagrams("iiii oiii ooii oooi oooo"), True)

    def test_count_valid_passphrases_advanced(self):
        count = count_valid_passphrases_advanced(
            [
                "abcde fghij",  # valid
                "abcde xyz ecdab",  # invalid
                "a ab abc abd abf abj",  # valid
                "iiii oiii ooii oooi oooo",  # valid
            ]
        )
        self.assertEquals(count, 3)
