#witam
import random, string
class RagBabyCipher:
    def gen_key(self):
        key_length = random.randint(3,40)
        word = ''.join(random.SystemRandom().choice(string.ascii_letters + ' ') for _ in range(key_length)).strip()
        alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzĘęĄąŚśĆćŻżŹźŁł'
        newWord = ''
        for x in alphabet:
            for y in word:
                if x == y:
                    alphabet = alphabet.replace(x, '')
        for x in word:
            if not x in newWord:
                newWord = newWord + x               
        newKey = newWord + alphabet
        return newKey
    
    def encrypt(self, text, key):
        encrypted = ""
        wordCount = 1
        num = 1
        for x in text:
            if x == ' ':
                encrypted += ' '
                wordCount += 1
                num = wordCount
            else:
                position = (key.find(x) + num)
                encrypted += key[position % (len(key))]
                num += 1
        return encrypted
    
    def decrypt(self, text, key):
        decrypted = ""
        wordCount = 1
        num = 1
        for x in text:
            if x == ' ':
                decrypted += ' '
                wordCount += 1
                num = wordCount 
            else:
                position = (key.find(x) - num + len(key))
                decrypted += key[position % len(key)]
                num += 1
        return decrypted

    def test(self):
        text_length = random.randint(100,200)
        key = self.gen_key()
        text = ''.join(random.SystemRandom().choice(string.ascii_letters + ' ') for _ in range(text_length)).strip()

        print(text)
        encrypted_text = self.encrypt(text, key)
        decrypted_text = self.decrypt(encrypted_text, key)
        print(decrypted_text)

