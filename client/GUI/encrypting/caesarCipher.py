import random, string
class CaesarCipher:

    def gen_key(self):
        shift = random.randint(2,65)
        return shift

    def get_cipherletter(self, new_key, letter):
        #still need alpha to find letters
        alpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĘęĄąŚśĆćŻżŹźŁł"

        if letter in alpha:
            return alpha[new_key]
        else:
            return letter

    def encrypt(self, key, message):
        alpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĘęĄąŚśĆćŻżŹźŁł"
        result = ""

        for letter in message:
            new_key = (alpha.find(letter) + key) % len(alpha)
            result = result + self.get_cipherletter(new_key, letter)

        return result

    def decrypt(self, key, message):
        alpha = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĘęĄąŚśĆćŻżŹźŁł"
        result = ""

        for letter in message:
            new_key = (alpha.find(letter) - key) % len(alpha)
            result = result + self.get_cipherletter(new_key, letter)

        return result

    def test(self):
        text_length = random.randint(100,200)
        text = ''.join(random.SystemRandom().choice(string.ascii_uppercase + ' ') for _ in range(text_length)).strip()
        key = self.gen_key()

        encrypted_text = self.encrypt(key, text)
        decrypted_text = self.decrypt(key, encrypted_text)

        print(decrypted_text)
