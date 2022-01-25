import re, random, string
class PolybiusSquareCipher:

    def generate_array(self, key=''):
        """Generates Polybius square"""
        abc = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ'
        abc += 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
        abc += '0123456789 '
        arr_el = []
        arr = []
        row = []
        if key:
            for char in key:
                if char not in arr_el:
                    arr_el.append(char)
            for char in abc:
                if char not in arr_el:
                    arr_el.append(char)
        else:
            arr_el = abc
        for i in range(9):
            for j in range(9):
                row.append(arr_el[i*9 + j])
            arr.append(row)
            row = []
        return arr
            
    def encrypt(self, word, key=''):
        """Encrypts message"""
        arr = self.generate_array(key)
        output = ''
        for char in word:
            for i in range(9):
                for j in range(9):
                    if char is arr[i][j]:
                        output+=str(j+1)
                        output+=str(i+1)
        return output

    def decrypt(self, word, key=''):
        """Decrypts message"""
        arr = self.generate_array(key)
        output = ''
        for i in range(int(len(word)/2)):
            col = int(word[i*2])
            row = int(word[i*2+1])
            letter = arr[row-1][col-1]
            output+=str(letter)
        return output

    def gen_key(self):
        key_length = random.randint(2,30)
        key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(key_length)).strip()
        return key
    
    def test(self):
        text_length = random.randint(100,200)
        key = self.gen_key()
        text = ''.join(random.SystemRandom().choice(string.ascii_letters + ' ') for _ in range(text_length)).strip()

        print(text)

        encrypted_text = self.encrypt(text, key)
        decrypted_text = self.decrypt(encrypted_text, key)

        print(decrypted_text)