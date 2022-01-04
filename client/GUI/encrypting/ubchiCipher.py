import random, string

class UbchiCipher: #dziala, wiadomosc odszyfrowana nie ma spacji :sadek:
    
    def keySequence(self,key):
        sequence = []
        for pos, ch in enumerate(key):
            lastletters = key[:pos]
            newnumber = 1
            for prevPos, prevCh in enumerate(lastletters):
                if prevCh > ch:
                    sequence[prevPos] += 1
                else:
                    newnumber += 1
            sequence.append(newnumber)
        return sequence

    def textInMatrix(self, string, key):
        lista1 = []
        lista2 = []
        ile = 0

        for x in string:
            lista1.append(x)
            ile = ile + 1
            if (ile % len(key) == 0):
                lista2.append(lista1.copy())
                lista1.clear()
                ile = 0
        if (ile % len(key) != 0):
            for y in range(0, len(key) - ile):
                lista1.append(' ')
            lista2.append(lista1.copy())
        return lista2

    def textFromMatrix(self, list, sekwencja, key, ileZnakowDodatkowych):
        finalMatrix = []
        column = []

        for x in range(1, len(sekwencja) + 1):
            index = sekwencja.index(x)
            for row in list:  # dodawanie kolumny
                if row[index] != ' ':  # kropka na spacje
                    column.append(row[index])
                if len(column) == len(key):
                    finalMatrix.append(column.copy())
                    column.clear()
        for i in range(ileZnakowDodatkowych):  # dodawanie kolumny
            literka = random.choice(string.ascii_letters)
            column.append(literka)
            if len(column) == len(key):
                finalMatrix.append(column.copy())
                column.clear()
        if (len(column) > 0):
            for j in range(len(key) - len(column)):
                column.append(' ')
            finalMatrix.append(column.copy())

        return finalMatrix

    def splitMatrix(self, list, sekwencja):
        string = ''
        ile = 0
        for x in range(1, len(sekwencja) + 1):
            index = sekwencja.index(x)
            for row in list:  # dodawanie kolumny
                if row[index] != ' ':
                    string += row[index]
                    ile = ile + 1

                if ile == 5:
                    ile = 0
                    string += " "
        return string

    def textIntoColumns(self, stringTmp, keyTmp, ileZnakowDodatkowych):
        keyTmp = keyTmp.lower()
        key = keyTmp.replace(" ", "")

        string = stringTmp.replace(" ", "")
        ilePelnychRzedow = int(len(string) / len(key))
        ileZnakowWOstatnim = len(string) % len(key)
        ileKolumn = len(key)
        ileWszystkichRzedow = ilePelnychRzedow + 1
        if ileZnakowWOstatnim == 0:
            ileWszystkichRzedow -= 1

        sekwencja = self.keySequence(key)

        matrix = []
        for i in range(ileWszystkichRzedow):
            row = []
            for j in range(ileKolumn):
                row.append(' ')
            matrix.append(row)
        indexik = 0

        for x in range(1, len(sekwencja) + 1):
            index = sekwencja.index(x)

            tmp = None
            if index < ileZnakowWOstatnim:
                tmp = ilePelnychRzedow + 1
            else:
                tmp = ilePelnychRzedow

            for i in range(tmp):
                matrix[i][index] = string[indexik]  # kolumna potem wiersz
                indexik += 1

        ileUsun = ileKolumn * ileWszystkichRzedow - indexik + ileZnakowDodatkowych
        return matrix, ileUsun

    def encrypt(self, text, keyTmp):
        keyTmp = keyTmp.lower()
        key = keyTmp.replace(" ", "")
        ileZnakowDodatkowych = len(keyTmp) - len(key) + 1
        text = text.lower().replace(" ", "")

        sekwencja = self.keySequence(key)
        lista = self.textInMatrix(text, key)
        finalLista = self.textFromMatrix(lista, sekwencja, key, ileZnakowDodatkowych)
        finalMessage = self.splitMatrix(finalLista, sekwencja)
        return finalMessage

    def decrypt(self, text, keyTmp):
        keyTmp = keyTmp.lower()
        key = keyTmp.replace(" ", "")
        ileZnakowDodatkowych = len(keyTmp) - len(key) + 1
        text = text.lower().replace(" ", "")

        decMatrix, ileUsun = self.textIntoColumns(text, key, ileZnakowDodatkowych)
        combinedText = ''.join(ele for sub in decMatrix for ele in sub)
        combinedText = combinedText[:-ileUsun]

        finalDecryptedMatrix, nic = self.textIntoColumns(combinedText, key, ileZnakowDodatkowych)

        decryptedText = ''.join(ele for sub in finalDecryptedMatrix for ele in sub)
        originalText = decryptedText.replace(" ", "")

        #finalText = ' '.join([originalText[i:i + 48] for i in range(0, len(originalText), 48)]) #zawijanie rzedami na sile, nie da sie inaczej tego zrobic

        return originalText
    
    def test(self):
        key_length = random.randint(10,20)
        text_length = random.randint(100,200)
        key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + ' ') for _ in range(key_length)).strip()
        text = ''.join(random.SystemRandom().choice(string.ascii_uppercase + ' ') for _ in range(text_length)).strip()

        encrypted_text = self.encrypt(text, key)
        decrypted_text = self.decrypt(encrypted_text, key)

        print(decrypted_text)

ubchi = UbchiCipher()
ubchi.test()