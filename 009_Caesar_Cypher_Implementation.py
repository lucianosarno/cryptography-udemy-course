# Alphabet will be used to convert letters into numerical values
# Including whitespace to be also converted into number
ALPHABET = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def caesar_encrypt(plain_text,key):
    cypher_text = ''
    plain_text = plain_text.upper()
    # Consider all individual letters in the plain text 
    for letter in plain_text:
        #Find the numerical representation of the letter
        index = ALPHABET.find(letter)
        new_index = index + key
        new_letter = ALPHABET[new_index % len(ALPHABET)]
        cypher_text += new_letter
    return cypher_text

def caesar_decrypt(cypher_text,key):
    plain_text = ''
    for letter in cypher_text:
        index = ALPHABET.find(letter)
        new_index = index - key
        new_letter = ALPHABET[new_index % len(ALPHABET)]
        plain_text += new_letter
    return plain_text

if __name__ == '__main__':
    plain_text = input('Enter the text to encrypt: ')
    key = int(input('Enter the key: '))
    cypher_text = caesar_encrypt(plain_text,key)
    print(f'Encrypted text: {cypher_text}')
    decrypted_text = caesar_decrypt(cypher_text,key)
    print(f'Decrypted text: {decrypted_text}')