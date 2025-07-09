import sys
import logging
from collections import Counter

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Alphabet (Uppercase as per lecture) ---
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_SIZE = len(ALPHABET)

# --- Expected Most Frequent Letter in English ---
# Based on standard English text frequency analysis (commonly 'E')
EXPECTED_MOST_FREQUENT = 'E'
EXPECTED_MOST_FREQUENT_INDEX = ALPHABET.index(EXPECTED_MOST_FREQUENT)

def frequency_analysis(text):
    """
    Performs frequency analysis on the given text, counting letter occurrences.
    Only considers letters present in the defined ALPHABET.
    Converts input text to uppercase.
    """
    logging.info("Starting frequency analysis...")
    # Convert text to uppercase as done in the lecture
    processed_text = text.upper()
    logging.debug(f"Processed text (uppercase): {processed_text[:50]}...") # Log a snippet

    # Initialize frequencies dictionary
    letter_frequencies = {letter: 0 for letter in ALPHABET}
    logging.debug(f"Initialized frequencies: {letter_frequencies}")

    # Count letter occurrences
    total_letters = 0
    for char in processed_text:
        if char in ALPHABET:
            letter_frequencies[char] += 1
            total_letters += 1

    logging.info(f"Frequency analysis complete. Total letters counted: {total_letters}")
    logging.debug(f"Calculated frequencies: {letter_frequencies}")
    return letter_frequencies

def find_most_frequent_letter(frequencies):
    """
    Finds the letter with the highest frequency from the analysis results.
    Handles ties by returning the first letter encountered with the max frequency.
    Returns None if frequencies dictionary is empty or contains only zero counts.
    """
    logging.info("Finding the most frequent letter...")
    if not frequencies:
        logging.warning("Frequency dictionary is empty.")
        return None

    # Find the letter with the maximum frequency
    # Use max with a key function to find the key (letter) based on the value (frequency)
    most_frequent_char = max(frequencies, key=frequencies.get)
    max_frequency = frequencies[most_frequent_char]

    if max_frequency == 0:
        logging.warning("No letters found in the text with non-zero frequency.")
        return None

    logging.info(f"Most frequent letter found: '{most_frequent_char}' with frequency {max_frequency}")
    return most_frequent_char

def calculate_key(most_frequent_in_ciphertext):
    """
    Calculates the Caesar cipher key based on the assumption that the most
    frequent letter in the ciphertext corresponds to the most frequent
    letter in English (E).
    Uses modular arithmetic.
    """
    logging.info(f"Calculating key assuming '{most_frequent_in_ciphertext}' corresponds to '{EXPECTED_MOST_FREQUENT}'...")

    if most_frequent_in_ciphertext not in ALPHABET:
         logging.error(f"Invalid character '{most_frequent_in_ciphertext}' for key calculation.")
         return None

    # Find the index of the most frequent letter in the ciphertext
    most_frequent_index = ALPHABET.index(most_frequent_in_ciphertext)
    logging.debug(f"Index of '{most_frequent_in_ciphertext}': {most_frequent_index}")
    logging.debug(f"Index of expected '{EXPECTED_MOST_FREQUENT}': {EXPECTED_MOST_FREQUENT_INDEX}")

    # The shift is the difference between their positions
    # We use the modulo operator (%) to handle wrap-around in the alphabet
    # (most_frequent_index - EXPECTED_MOST_FREQUENT_INDEX) is the shift amount.
    # If the most frequent is 'F' (index 5) and expected is 'E' (index 4), shift is 1.
    # If the most frequent is 'C' (index 2) and expected is 'E' (index 4), shift is -2.
    # The key for decryption is this shift amount.
    key = (most_frequent_index - EXPECTED_MOST_FREQUENT_INDEX) % ALPHABET_SIZE

    logging.info(f"Calculated key (shift amount for decryption): {key}")
    # The key represents how many positions each letter in the ciphertext was shifted *forward*
    # from the original plaintext letter. So, to decrypt, we shift *backward* by this amount.
    # The calculation (most_frequent_index - EXPECTED_MOST_FREQUENT_INDEX) % ALPHABET_SIZE
    # directly gives the required *backward* shift to get from the ciphertext letter to the plaintext 'E'.
    # For example, if 'X' (index 23) is most frequent (should be 'E', index 4):
    # (23 - 4) % 26 = 19 % 26 = 19. This means 'X' was shifted 19 positions forward from 'E'
    # (E -> F -> ... -> X). So the key used for encryption was 19.
    # To decrypt 'X', we shift it back 19 positions: (23 - 19) % 26 = 4, which is 'E'.
    # So the calculated value IS the key to SUBTRACT during decryption.

    return key

def decrypt_text(ciphertext, key):
    """
    Decrypts the Caesar cipher text using the calculated key (shift amount).
    Non-alphabetic characters are left unchanged.
    Handles uppercase letters as processed by frequency analysis.
    """
    logging.info(f"Decrypting text with key (backward shift): {key}")
    decrypted_text = ""
    processed_text = ciphertext.upper() # Ensure consistency with analysis

    for char in processed_text:
        if char in ALPHABET:
            # Find the character's index in the alphabet
            char_index = ALPHABET.index(char)
            # Shift the index backward by the key amount (modulo 26)
            # The result is the index of the original plaintext letter
            decrypted_index = (char_index - key) % ALPHABET_SIZE
            # Get the plaintext letter from the decrypted index
            plaintext_char = ALPHABET[decrypted_index]
            decrypted_text += plaintext_char
            logging.debug(f"Decrypted '{char}' (index {char_index}) with key {key} to '{plaintext_char}' (index {decrypted_index})")
        else:
            # Keep non-alphabetic characters as they are
            decrypted_text += char
            logging.debug(f"Keeping non-alphabetic character: '{char}'")

    logging.info("Decryption complete.")
    logging.info(f"Decrypted text: {decrypted_text}")
    return decrypted_text

# --- Main execution block ---
if __name__ == "__main__":
    # Check for command line argument
    if len(sys.argv) != 2:
        logging.error("Usage: python3 your_script_name.py \"Encrypted Text Here\"")
        # Exit if no text is provided
        sys.exit(1)

    # Get the ciphertext from the command line argument
    ciphertext_input = sys.argv[1]
    logging.info(f"Received ciphertext from command line: \"{ciphertext_input}\"")

    # Perform frequency analysis on the ciphertext
    frequencies = frequency_analysis(ciphertext_input)

    # Find the most frequent letter in the ciphertext
    most_frequent_cipher = find_most_frequent_letter(frequencies)

    if most_frequent_cipher is None:
        logging.error("Could not determine the most frequent letter. Cannot proceed with cracking.")
        sys.exit(1)

    # Calculate the potential key
    # Note: This assumes the most frequent letter *is* 'E'. This is an heuristic.
    calculated_key = calculate_key(most_frequent_cipher)

    if calculated_key is None:
         logging.error("Failed to calculate key.")
         sys.exit(1)

    # Decrypt the text using the calculated key
    decrypted_text = decrypt_text(ciphertext_input, calculated_key)