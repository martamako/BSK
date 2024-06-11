from Szyfrowanie.Szyfrowanie import Szyfrowanie
from cryptography.fernet import Fernet


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#def szyfrowanie():
#    key = Fernet.generate_key()
#    with open("mykey.key", "wb") as f:
#        f.write(key)

def getting_key():
    with open("mykey.key", "rb") as f:
        key = f.read()
        return key

def encrypting_file(key: Fernet):
    with open("private.pem", "rb") as private_pem:
        private_key = private_pem.read()
    encrypted = key.encrypt(private_key)

    with open("private.pem", "wb") as encrypted_file:
        encrypted_file.write(encrypted)

def decrypting_file(key: Fernet):
    with open("private.pem", "rb") as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = key.decrypt(encrypted)
    with open("private.pem", "wb") as decrypted_file:
        decrypted_file.write(decrypted)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # szyfrowanie_publiczne = Szyfrowanie()
    print_hi('PyCharm')
    #key = getting_key()
    # encrypting_file(Fernet(key))
    #decrypting_file(Fernet(key))



