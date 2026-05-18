from collections import Counter
import numpy as np

ENGLISH_FREQ = {
    'E': 12.7,
    'T': 9.1,
    'A': 8.2,
    'O': 7.5,
    'I': 7.0,
    'N': 6.7,
    'S': 6.3,
    'H': 6.1,
    'R': 6.0,
    'D': 4.3,
    'L': 4.0,
    'C': 2.8,
    'U': 2.8,
    'M': 2.4,
    'W': 2.4,
    'F': 2.2,
    'G': 2.0,
    'Y': 2.0,
    'P': 1.9,
    'B': 1.5,
    'V': 1.0,
    'K': 0.8,
    'J': 0.15,
    'X': 0.15,
    'Q': 0.10,
    'Z': 0.07
}


def clean_text(text):
    return ''.join(c.upper() for c in text if c.isalpha())


# -------------------------------------------------
# LETTER COUNTING
# -------------------------------------------------

def count_letters(text):
    text = clean_text(text)
    return Counter(text)


# -------------------------------------------------
# FREQUENCY CALCULATION
# -------------------------------------------------

def calculate_frequency(text):
    text = clean_text(text)

    total = len(text)

    if total == 0:
        return {}

    counts = Counter(text)

    frequencies = {}

    for letter, count in counts.items():
        frequencies[letter] = round((count / total) * 100, 2)

    return frequencies


# -------------------------------------------------
# SUGGEST LIKELY LETTER MAPPINGS
# -------------------------------------------------

def suggest_mappings(ciphertext):

    freq = calculate_frequency(ciphertext)

    sorted_cipher = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    english_sorted = sorted(
        ENGLISH_FREQ.items(),
        key=lambda x: x[1],
        reverse=True
    )

    suggestions = {}

    for i in range(min(len(sorted_cipher), len(english_sorted))):
        cipher_letter = sorted_cipher[i][0]
        english_letter = english_sorted[i][0]

        suggestions[cipher_letter] = english_letter

    return suggestions