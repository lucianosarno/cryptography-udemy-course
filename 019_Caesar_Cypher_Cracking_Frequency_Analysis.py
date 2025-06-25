import matplotlib.pyplot as plt
import string
import logging # Import the logging module
import sys

# Configure logging
# Log messages with level INFO or higher will be displayed
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def frequency_analysis(text):
    """Calculates the frequency of each letter in a given text."""
    alphabet = string.ascii_uppercase
    letter_frequencies = {}

    for letter in alphabet:
        letter_frequencies[letter] = 0

    upper_text = text.upper()
    total_letters_counted = 0 # To count how many letters were actually analyzed
    for letter in upper_text:
        if letter in alphabet:
            letter_frequencies[letter] += 1
            total_letters_counted += 1

    # Optional: Log the raw frequencies (can be verbose for long texts)
    # logging.debug(f"Raw frequencies: {letter_frequencies}")
    logging.info(f"Frequency analysis completed for {total_letters_counted} letters.")
    return letter_frequencies

def plot_distribution(frequencies):
    """Plots the frequency distribution."""
    logging.info("Generating frequency distribution plot.")
    sorted_letters = sorted(frequencies.keys())
    sorted_frequencies = [frequencies[letter] for letter in sorted_letters]

    plt.bar(sorted_letters, sorted_frequencies)
    plt.xlabel("Letters")
    plt.ylabel("Frequency")
    plt.title("Letter Frequency Distribution")
    plt.show()
    logging.info("Plot displayed.")

def caesar_crack_frequency(ciphertext):
    """
    Cracks a Caesar cipher using frequency analysis.
    Assumes 'E' is the most frequent letter in the original plaintext.
    """
    logging.info(f"Starting frequency analysis-based cracking.")
    logging.info(f"Input ciphertext (first 50 chars): {ciphertext[:50]}{'...' if len(ciphertext) > 50 else ''}")

    alphabet = string.ascii_uppercase
    index_E = alphabet.find('E') # Index of 'E' is 4

    cipher_frequencies = frequency_analysis(ciphertext)

    if not cipher_frequencies or all(freq == 0 for freq in cipher_frequencies.values()):
        logging.warning("Ciphertext contains no letters from the alphabet. Cannot perform frequency analysis.")
        return "Cannot analyze text without letters.", None # Return None for key

    # Find the most frequent letter in the ciphertext
    # Filter out letters with zero frequency to avoid issues with max() on empty results if no letters were found
    non_zero_frequencies = {letter: freq for letter, freq in cipher_frequencies.items() if freq > 0}

    if not non_zero_frequencies:
         logging.warning("Frequency analysis found no letters with non-zero counts. Cannot determine most frequent letter.")
         return "No countable letters found for frequency analysis.", None

    most_frequent_cipher_letter = max(non_zero_frequencies, key=non_zero_frequencies.get)
    logging.info(f"Most frequent letter in ciphertext: {most_frequent_cipher_letter}")

    # Determine the shift (key)
    index_most_frequent_cipher = alphabet.find(most_frequent_cipher_letter)

    # Calculate shift. Shift = (Index of most frequent cipher letter - Index of assumed most frequent plaintext letter ('E')) mod 26
    shift = (index_most_frequent_cipher - index_E) % 26
    logging.info(f"Assuming original 'E' (index {index_E}) maps to '{most_frequent_cipher_letter}' (index {index_most_frequent_cipher}).")
    logging.info(f"Calculated shift (key): {shift}")

    # Decrypt the ciphertext using the calculated shift
    decrypted_text = ""
    logging.info(f"Decrypting ciphertext using shift {shift}.")
    for char in ciphertext.upper():
        if char in alphabet:
            original_index = alphabet.find(char)
            # Reverse the shift: (original_index - shift) mod 26
            decrypted_index = (original_index - shift) % 26
            decrypted_char = alphabet[decrypted_index]
            decrypted_text += decrypted_char
        else:
            decrypted_text += char # Keep non-alphabetic characters as they are

    logging.info("Decryption complete.")
    return decrypted_text, shift

# Example Usage:
if __name__ == "__main__":
    logging.info("--- Script Start ---")

    # Example from the lecture (Shannon's secrecy text, modified for clarity)
    plain_example = "THIS IS A TEST TEXT TO DEMONSTRATE FREQUENCY ANALYSIS"
    # Let's simulate encrypting it with a Caesar shift, say, 3 (D -> A, E -> B, etc.)
    # A shift of 3 means A becomes D, B becomes E, etc. Original E becomes H.
    cipher_example = "WKLV LV D WHVW WHAW WR GHPRQVWUDWH IUHTXHQFB DQDOBVLV"

    logging.info("--- Frequency Analysis on Plain Text ---")
    plain_frequencies = frequency_analysis(plain_example)
    # plot_distribution(plain_frequencies) # Uncomment to show plot for plaintext

    logging.info("\n--- Cracking Cipher Text Example 1 ---")
    cracked_text, key_found = caesar_crack_frequency(cipher_example)
    print(f"\nCracked Text (Example 1): {cracked_text}")
    print(f"Key found (Example 1): {key_found}")

    # Example with a known Caesar cipher text (Shift 3: ATTACK -> DWWDFA)
    known_cipher = "DWWDFA"
    logging.info("\n--- Cracking Known Cipher Example 2 (DWWDFA) ---")
    cracked_known, key_found_known = caesar_crack_frequency(known_cipher)
    print(f"\nCracked Text (Example 2): {cracked_known}")
    print(f"Key found (Example 2): {key_found_known}") # Should find key 3 and decrypt to ATTACK

    logging.info("--- Script End ---")
    
    
# Main execution block
if __name__ == "__main__":
    # Check if a command-line argument was provided
    if len(sys.argv) > 1:
        # If yes, use the first argument as the ciphertext
        input_ciphertext = sys.argv[1]
        print(f"[*] Using ciphertext provided via command line: '{input_ciphertext}'")
    else:
        # If no argument was provided, use the default hardcoded example
        input_ciphertext = "khoorzcruog" # Or "vjku bkscuug" from the lecture example
        print(f"[*] No command-line argument provided. Using default example ciphertext: '{input_ciphertext}'")

    # Now call the cracking function with the selected ciphertext
    frequency_analysis(input_ciphertext)