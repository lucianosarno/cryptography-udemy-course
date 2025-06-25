import sys

# Define the alphabet including whitespace, matching the lecture's description
# This determines the size of the search space for the key
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ' # Assuming lowercase and space

def crack_caesar(ciphertext):
    """
    Attempts to crack a Caesar cipher encrypted message using a brute force approach.
    It tries every possible key value from 0 up to the length of the alphabet - 1.

    Args:
        ciphertext (str): The encrypted message to crack.
    """
    print(f"[*] Starting brute force crack for ciphertext: '{ciphertext}'")
    print(f"[*] Alphabet used: '{ALPHABET}' (Length: {len(ALPHABET)})")
    print("[*] Trying all possible keys...")

    # Brute force involves trying every possible key
    # The number of possible keys is equal to the size of the alphabet
    # because shifting by len(ALPHABET) is the same as shifting by 0 (due to modulo)
    for key in range(len(ALPHABET)):
        # For each key, we attempt to decrypt the entire ciphertext
        potential_plaintext = ""
        print(f"\n[+] Trying Key = {key}")
        print("    [+] Decrypting character by character...")

        # Iterate through each character in the ciphertext
        for char in ciphertext:
            # Find the numerical index of the character in the alphabet
            # We assume the character exists in our defined ALPHABET
            char_index = ALPHABET.find(char)

            # --- Applied Math Point: Modular Arithmetic ---
            # The core decryption formula: (original_index - key) % len(ALPHABET)
            # Modulo (%) ensures that the result wraps around the alphabet length.
            # E.g., if ALPHABET is 27 chars, index 0, key 1, (0-1)%27 = -1%27 = 26.
            # This brings us back to the end of the alphabet.
            # This is the inverse operation of the encryption: (original_index + key) % len(ALPHABET)
            original_index = (char_index - key) % len(ALPHABET)

            # Get the character from the alphabet using the calculated original index
            decrypted_char = ALPHABET[original_index]

            # Append the decrypted character to the potential plaintext
            potential_plaintext += decrypted_char

            # Log the step for this character
            print(f"        Char: '{char}' (Index: {char_index}) -> Calculation: ({char_index} - {key}) % {len(ALPHABET)} = {original_index} -> Decrypted: '{decrypted_char}'")

        # After processing all characters with the current key, print the result
        print(f"    [-] Result for Key {key}: '{potential_plaintext}'")

        # In a real-world scenario (beyond this simple example), you'd need a way
        # to automatically detect if 'potential_plaintext' makes sense (e.g., frequency analysis,
        # dictionary attack, checking for common words). Here, we rely on manual inspection
        # as shown in the lecture.

    print("\n[*] Brute force process finished.")
    print("[*] Review the results above to find the plaintext that makes sense.")

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
    crack_caesar(input_ciphertext)