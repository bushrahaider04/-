# transposition.py
from collections import Counter
# -------------------------------------------------
# INDEX OF COINCIDENCE
# -------------------------------------------------
def calculate_ic(text):

    text = ''.join(c.upper() for c in text if c.isalpha())
#Hello 123!
    N = len(text)

    if N <= 1:
        return 0

    counts = Counter(text)

    numerator = sum(f * (f - 1) for f in counts.values())

    denominator = N * (N - 1)

    return numerator / denominator


# -------------------------------------------------
# FACTOR POSSIBLE GRID SIZES
# -------------------------------------------------
def factor_text_length(length):

    factors = []

    for i in range(2, length + 1):

        if length % i == 0:
            factors.append((i, length // i))

    return factors


# -------------------------------------------------
# TRANSPOSITION DETECTION
# -------------------------------------------------
def detect_transposition(text):

    ic = calculate_ic(text)

    if 0.055 <= ic <= 0.075:
        return (
            True,
            f"Likely Transposition Cipher Detected. IC = {round(ic, 4)}"
        )
    return (
        False,
        f"Transposition Cipher Unlikely. IC = {round(ic, 4)}"
    )

