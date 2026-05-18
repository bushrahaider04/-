from frequency import calculate_frequency, ENGLISH_FREQ

# -------------------------------------------------
# CAESAR DECRYPTION
# -------------------------------------------------

def decrypt_caesar(ciphertext, shift):

    result = ""

    for char in ciphertext:

        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')

            result += chr((ord(char) - start - shift) % 26 + start)

        else:
            result += char

    return result


# -------------------------------------------------
# CHI-SQUARED SCORING
# -------------------------------------------------

def chi_squared_score(text):

    frequencies = calculate_frequency(text)

    score = 0

    for letter in ENGLISH_FREQ:

        observed = frequencies.get(letter, 0)
        expected = ENGLISH_FREQ[letter]

        score += ((observed - expected) ** 2) / expected

    return score


# -------------------------------------------------
# BRUTE FORCE ALL 26 SHIFTS
# -------------------------------------------------

def brute_force_caesar(ciphertext):

    results = []

    for shift in range(26):

        decrypted = decrypt_caesar(ciphertext, shift)

        score = chi_squared_score(decrypted)

        results.append({
            "shift": shift,
            "text": decrypted,
            "score": round(score, 2)
        })

    results.sort(key=lambda x: x["score"])

    best_score = results[0]["score"]

    for result in results:

        confidence = max(0, 100 - (result["score"] - best_score))

        result["confidence"] = round(confidence, 2)

    return results[:3]

