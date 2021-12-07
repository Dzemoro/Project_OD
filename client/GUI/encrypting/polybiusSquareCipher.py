import re, random, string
class PolybiusSquareCipher:

    def unPolishText(self, text):
        """Converts Polish letters to Latin"""
        polish = "ĄĆĘŁŃÓŚŹŻ"
        normal = "ACELNOSZZ"
        table = text.maketrans(polish, normal)
        return text.translate(table)


    def generate_array(self, key=''):
        """Generates Polybius square"""
        abc = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        arr_el=[]
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
        for i in range(5):
            for j in range(5):
                row.append(arr_el[i*5 + j])
            arr.append(row)
            row = []
        return arr
            
    def encrypt(self, word, key=''):
        """Encrypts message"""
        word = word.upper()
        key = key.upper()
        word = re.sub(r'J','I', word)
        key = re.sub(r'J','I', key)
        word = self.unPolishText(word)
        key = self.unPolishText(key)
        word = re.sub('[^A-Z]','', word)
        key = re.sub('[^A-Z]','', key)
        arr = self.generate_array(key)
        output = ''
        for char in word:
            for i in range(5):
                for j in range(5):
                    if char is arr[i][j]:
                        output+=str(j+1)
                        output+=str(i+1)
        return output

    def decrypt(self, word, key=''):
        """Decrypts message"""
        word = word.upper()
        key = key.upper()
        key = re.sub(r'J','I', key)
        key = self.unPolishText(key)
        key = re.sub('[^A-Z]','', key)
        arr = self.generate_array(key)
        output = ''
        for i in range(int(len(word)/2)):
            col = int(word[i*2])
            row = int(word[i*2+1])
            letter = arr[row-1][col-1]
            output+=str(letter)
        return output
    
    def test(self):
        key_length = random.randint(10,20)
        text_length = random.randint(100,200)
        key = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(key_length)).strip()
        text = ''.join(random.SystemRandom().choice(string.ascii_uppercase + ' ') for _ in range(text_length)).strip()

        encrypted_text = self.encrypt(text, key)
        decrypted_text = self.decrypt(encrypted_text, key)

        print(decrypted_text)
    
    

polybius = PolybiusSquareCipher()
polybius.test()