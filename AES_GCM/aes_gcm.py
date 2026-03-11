from os import urandom  
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = urandom(16)
NONCE = urandom(12)

def aes_gcm_encrypt(plaintext, KEY):
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext.hex(), tag.hex()

def aes_gcm_decrypt(ciphertext, tag, KEY):
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext 

pt1 = b'AESGCM keeps data safe and sound'
pt2 = urandom(32)

print('hint 1: ',aes_gcm_encrypt(pt1, key))
print('hint 2: ',aes_gcm_encrypt(pt2, key))

challenge = urandom(32).hex()
print("Prove you have the decryption key by encrypting this challenge and giving the valid ciphertext and authentication tag.")
print('Challenge: ', challenge)

secret_message = "..."

while True:
    ct = input('Enter ciphertext: ')
    tag = input('Enter tag: ')
    try:
        pt = aes_gcm_decrypt(bytes.fromhex(ct), bytes.fromhex(tag), key)

        if pt.hex() == challenge:
            print('secret message: ', secret_message)
            break
            
    except:
        print('invalid value')
        pass