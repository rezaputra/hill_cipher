import numpy as np

class HillCipher():
    def __init__(self, msg):
        assert len(msg) >= 0, f"message cannot be empty"
        assert len(msg) <= 200, f"message is too long"
        assert type(msg) == str, f"message should be a string"

        self.__msg = msg

    @property
    def msg(self):
        return self.__msg

    @msg.setter
    def msg(self, value):
        if not value:
            raise Exception("The name is empty!")
        elif len(value) <= 0:
            raise Exception("The name is too short !")
        elif len(value) >= 200:
            raise Exception("The name is too long !")
        else:
            self.__msg = value

    def chr_to_int(self, char):
        # Uppercase the char to get into range 65-90 in ascii table
        char = char.upper()
        # Cast chr to int and subtract 65 to get 0-25
        integer = ord(char) - 65
        return integer
    
    def create_matrix_of_integers_from_string(self, string):
        # Map string to a list of integers a/A <-> 0, b/B <-> 1 ... z/Z <-> 25
        integers = [self.chr_to_int(c) for c in string]
        length = len(integers)
        M = np.zeros((2, int(length / 2)), dtype=np.int32)
        iterator = 0
        for column in range(int(length / 2)):
            for row in range(2):
                M[row][column] = integers[iterator]
                iterator += 1
        return M

    def find_multiplicative_inverse(self, determinant):
        multiplicative_inverse = -1
        for i in range(26):
            inverse = determinant * i
            if inverse % 26 == 1:
                multiplicative_inverse = i
                break
        return multiplicative_inverse
    
    def make_key(self):
        # Make sure cipher determinant is relatively prime to 26 and only a/A - z/Z are given
        determinant = 0
        C = None
        while True:
            cipher = input("Input 4 letter cipher: ")
            C = self.create_matrix_of_integers_from_string(cipher)
            determinant = C[0][0] * C[1][1] - C[0][1] * C[1][0]
            determinant = determinant % 26
            inverse_element = self.find_multiplicative_inverse(determinant)
            if inverse_element == -1:
                print("Determinant is not relatively prime to 26, uninvertible key")
            elif np.amax(C) > 26 and np.amin(C) < 0:
                print("Only a-z characters are accepted")
                print(np.amax(C), np.amin(C))
            else:
                break
        return C


    def encrypt(self):
        # Replace spaces with nothing
        msg = self.__msg.replace(" ", "")
        # Ask for keyword and get encryption matrix
        C = self.make_key()
        # Append zero if the messsage isn't divisble by 2
        len_check = len(self.__msg) % 2 == 0
        if not len_check:
            self.__msg += "0"
        # Populate message matrix
        P = self.create_matrix_of_integers_from_string(self.__msg)
        # Calculate length of the message
        msg_len = int(len(self.__msg) / 2)
        # Calculate P * C
        encrypted_msg = ""
        for i in range(msg_len):
            # Dot product
            row_0 = P[0][i] * C[0][0] + P[1][i] * C[0][1]
            # Modulate and add 65 to get back to the A-Z range in ascii
            integer = int(row_0 % 26 + 65)
            # Change back to chr type and add to text
            encrypted_msg += chr(integer)
            # Repeat for the second column
            row_1 = P[0][i] * C[1][0] + P[1][i] * C[1][1]
            integer = int(row_1 % 26 + 65)
            encrypted_msg += chr(integer)
        return encrypted_msg


    def decrypt(self):
        # Ask for keyword and get encryption matrix
        C = self.make_key()
        # Inverse matrix
        determinant = C[0][0] * C[1][1] - C[0][1] * C[1][0]
        determinant = determinant % 26
        multiplicative_inverse = self.find_multiplicative_inverse(determinant)
        C_inverse = C
        # Swap a <-> d
        C_inverse[0][0], C_inverse[1][1] = C_inverse[1, 1], C_inverse[0, 0]
        # Replace
        C[0][1] *= -1
        C[1][0] *= -1
        for row in range(2):
            for column in range(2):
                C_inverse[row][column] *= multiplicative_inverse
                C_inverse[row][column] = C_inverse[row][column] % 26

        P = self.create_matrix_of_integers_from_string(self.__msg)
        msg_len = int(len(self.__msg) / 2)
        decrypted_msg = ""
        for i in range(msg_len):
            # Dot product
            column_0 = P[0][i] * C_inverse[0][0] + P[1][i] * C_inverse[0][1]
            # Modulate and add 65 to get back to the A-Z range in ascii
            integer = int(column_0 % 26 + 65)
            # Change back to chr type and add to text
            decrypted_msg += chr(integer)
            # Repeat for the second column
            column_1 = P[0][i] * C_inverse[1][0] + P[1][i] * C_inverse[1][1]
            integer = int(column_1 % 26 + 65)
            decrypted_msg += chr(integer)
        if decrypted_msg[-1] == "0":
            decrypted_msg = decrypted_msg[:-1]
        return decrypted_msg    

    
# hill = HillCipher("INI BUDI")
# print(hill.encrypt())

# hill = HillCipher("BUDI SUKA BELAJAR")
# print(hill.encrypt())

# hill = HillCipher("HILL CIPHER")
# print(hill.encrypt())

# cipher = HillCipher("DYJWWFOP")
# print(cipher.decrypt())

# cipher = HillCipher("WFOPEZYWTYGTWHSBRJ")
# print(cipher.decrypt())

# cipher = HillCipher("WBHZONFGSLRJ")
# print(cipher.decrypt())