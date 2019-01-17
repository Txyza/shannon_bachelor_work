from Cryptodome.PublicKey import RSA

code = 'PINLOX!@#FYnjybjy12QWElkjPOasd$!@$fffffffasdasd'
key = RSA.generate(2048)

encrypted_key = key.exportKey(
    passphrase=code,
    pkcs=8,
    protection="scryptAndAES128-CBC"
)

with open('my_private_rsa_key.bin', 'wb') as f:
    f.write(encrypted_key)

with open('my_rsa_public.pem', 'wb') as f:
    f.write(key.publickey().exportKey())
