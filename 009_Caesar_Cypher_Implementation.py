import logging

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Alphabet will be used to convert letters into numerical values
# Including whitespace to be also converted into number
ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def caesar_encrypt(plain_text,key):
    logging.info(f"Encrypting text: {plain_text} with key: {key}")
    cypher_text = ''
    plain_text = plain_text.upper()
    logging.debug(f"Uppercase text: {plain_text}")
    # Consider all individual letters in the plain text
    for letter in plain_text:
        #Find the numerical representation of the letter
        index = ALPHABET.find(letter)
        logging.debug(f"Letter: {letter}, index: {index}")
        new_index = index + key
        logging.debug(f"New index: {new_index}")
        new_letter = ALPHABET[new_index % len(ALPHABET)]
        logging.debug(f"New letter: {new_letter}")
        cypher_text += new_letter
    logging.info(f"Encrypted text: {cypher_text}")
    return cypher_text

def caesar_decrypt(cypher_text,key):
    logging.info(f"Decrypting text: {cypher_text} with key: {key}")
    plain_text = ''
    for letter in cypher_text:
        index = ALPHABET.find(letter)
        logging.debug(f"Letter: {letter}, index: {index}")
        new_index = index - key
        logging.debug(f"New index: {new_index}")
        new_letter = ALPHABET[new_index % len(ALPHABET)]
        logging.debug(f"New letter: {new_letter}")
        plain_text += new_letter
    logging.info(f"Decrypted text: {plain_text}")
    return plain_text

if __name__ == '__main__':
    plain_text = input('Enter the text to encrypt: ')
    key = int(input('Enter the key: '))
    logging.info(f"Plain text: {plain_text}, key: {key}")
    cypher_text = caesar_encrypt(plain_text,key)
    print(f'Encrypted text: {cypher_text}')
    decrypted_text = caesar_decrypt(cypher_text,key)
    print(f'Decrypted text: {decrypted_text}')
    logging.info(f"Plain text: {plain_text}, key: {key}, Encrypted text: {cypher_text}, Decrypted text: {decrypted_text}")