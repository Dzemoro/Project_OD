import random, string
class CaesarCipher:
    def get_cipherletter(self, new_key, letter):
        #still need alpha to find letters
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if letter in alpha:
            return alpha[new_key]
        else:
            return letter

    def encrypt(self, key, message):
        message = message.upper()
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in message:
            new_key = (alpha.find(letter) + key) % len(alpha)
            result = result + self.get_cipherletter(new_key, letter)

        return result

    def decrypt(self, key, message):
        message = message.upper()
        alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""

        for letter in message:
            new_key = (alpha.find(letter) - key) % len(alpha)
            result = result + self.get_cipherletter(new_key, letter)

        return result

    def test(self):
        text_length = random.randint(100,200)
        text = ''.join(random.SystemRandom().choice(string.ascii_uppercase + ' ') for _ in range(text_length)).strip()

        encrypted_text = self.encrypt(3, text)
        decrypted_text = self.decrypt(3, encrypted_text)

        print(decrypted_text)

caesar = CaesarCipher()
caesar.test()