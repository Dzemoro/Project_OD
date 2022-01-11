from cryptography.fernet import Fernet

class FernetCipher:

    def gen_key(self):
        key = Fernet.generate_key()
        return key

    def encrypt(self, message, key):
        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())
        return encMessage
    
    def decrypt(self, message, key):
        fernet = Fernet(key)
        decMessage = fernet.decrypt(bytes(message)).decode()
        return decMessage