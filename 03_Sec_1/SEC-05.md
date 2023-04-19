# Asymmetric Encryption
Asymmetric encryption, also known as public key cryptography, is a method of encrypting digital information using a pair of keys - a public key and a private key - that are mathematically related but not identical. The public key is widely available and can be used by anyone to encrypt messages, while the private key is kept secret and is used to decrypt the messages that are encrypted with the public key.

## Key-terms
**Public key**

The public key is used for encryption. It is made freely available to anyone who wants to send an encrypted message to the owner of the key. When someone encrypts a message using the public key, only the private key holder can decrypt and read the message.

**Private key**

The private key is used for decryption. It is kept secret by the owner of the key and is used to decrypt messages that have been encrypted using the corresponding public key. The private key must be kept secret to ensure that only the intended recipient can decrypt and read the message.

## Opdracht
- Generate a key pair.

- Send an asymmetrically encrypted message to one of your peers via the public Slack channel. They should be able to decrypt the message using a key. The recipient should be able to read the message, but it should remain a secret to everyone else. You are not allowed to use any private messages or other communication channels besides the public Slack channel. Analyse the difference between this method and symmetric encryption.

### Gebruikte bronnen
ChatGPT

https://travistidwell.com/jsencrypt/demo/

https://www.devglan.com/online-tools/rsa-encryption-decryption

### Ervaren problemen
None

### Resultaat
I have successfully generated a key pair.

Based on what I have expirienced when it comes to the Symmetrical and Asymmetrical encryptions it clearly shows that the Symmetrical one has the possiblity to be decrypted by someone that figured out your method.

But when it comes to Asymmetrical, there is no possible way anyone that does not have your private key can decrypt it. It also adds a level of security to the message of those sending it to you.
