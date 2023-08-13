from typing import List


def count_valid_passphrases_basic(passphrases: List[str]) -> int:
    return len([phrase for phrase in passphrases if contains_unique_words(phrase)])


def count_valid_passphrases_advanced(passphrases: List[str]) -> int:
    return len([phrase for phrase in passphrases if contains_unique_anagrams(phrase)])


def contains_unique_words(passphrase: str) -> bool:
    words = passphrase.split()
    return len(set(words)) == len(words)


def contains_unique_anagrams(passphrase: str) -> bool:
    words = passphrase.split()
    words_with_sorted_letters_set = {"".join(sorted(w)) for w in words}
    return len(words_with_sorted_letters_set) == len(words)
