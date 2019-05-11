from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Random import get_random_bytes
from Cryptodome.PublicKey import RSA
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice

re_text = ascii_uppercase+ascii_lowercase+digits
print(re_text)

for i in range(1, 256):
    data = ''.join(choice(re_text) for _ in range(736*68))
    with open('..\\test\\{}'.format(i), 'wb') as out_file:
        recipient_key = RSA.import_key(
            open('key\\my_rsa_public.pem').read()
        )
        session_key = get_random_bytes(32)

        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        out_file.write(cipher_rsa.encrypt(session_key))

        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        data = data.encode()
        ciphertext, tag = cipher_aes.encrypt_and_digest(data)
        out_file.write(cipher_aes.nonce)
        out_file.write(tag)
        out_file.write(ciphertext)
