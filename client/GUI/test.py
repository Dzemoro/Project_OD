from encrypting.fernet import FernetCipher
from encrypting.caesarCipher import CaesarCipher
from encrypting.polybiusSquareCipher import PolybiusSquareCipher
from encrypting.RagBabyCipher import RagBabyCipher

class Test:
    def exchange_keys(self):
        self.caesar = CaesarCipher()
        self.fernet = FernetCipher()
        self.polybius = PolybiusSquareCipher()
        self.rag_baby = RagBabyCipher()

        #keys generation
        caesar_key = self.caesar.gen_key()
        fernet_key = self.fernet.gen_key()
        polybius_key = self.polybius.gen_key()
        rag_baby_key = self.rag_baby.gen_key()
        #keys = str(caesar_key) + ":" + str(fernet_key) + ":" + str(polybius_key) + ":" + str(rag_baby_key)
        message = "Przeprowadzka do nowego miasta to zawsze wielka niewiadoma" #4 23$ :d 31 ,./" #poprawic znaki specjalne?

        #encrypting
        caesar_message = self.caesar.encrypt(key = caesar_key, message = message)
        fernet_message = self.fernet.encrypt(key = fernet_key, message = message)
        polybius_message = self.polybius.encrypt(key = polybius_key, word = message)
        rag_baby_message = self.rag_baby.encrypt(key = rag_baby_key, text = message)

        #decrypting
        caesar_message = self.caesar.decrypt(caesar_key, caesar_message)
        fernet_message = self.fernet.decrypt(fernet_message, fernet_key)
        polybius_message = self.polybius.decrypt(polybius_message, polybius_key)
        rag_baby_message = self.rag_baby.decrypt(rag_baby_message, rag_baby_key)

        print(message)
        print(caesar_message)
        print(fernet_message)
        print(polybius_message)
        print(rag_baby_message)

test = Test()
test.exchange_keys()
