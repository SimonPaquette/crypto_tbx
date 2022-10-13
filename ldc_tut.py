"""
Cryptography using SPN cipher
Able to encryt a binary message with tools like Sboxes, Substition layers and Transposition layers.
"""
import numpy as np


def _bin(dec_val: int, length: int) -> str:
    """
    Convert a decimal value to a string binary

    Args:
        dec_val (int): decimal value to convert
        length (int): total length of the binary string

    Returns:
        str: binary string
    """
    return format(dec_val, f"0{length}b")


def _dec(bin_val: str) -> int:
    """
    Convert a binary value to a decimal value

    Args:
        bin_val (str): binary string

    Returns:
        int: decimal representation
    """
    return int(bin_val, 2)


class SBox_4:
    """
    A 4x4 S-box (substitution-box).
    """

    def __init__(self, *values):
        assert len(values) % 4 == 0
        self.values = list(values)
        self.length = len(values) // 4

    def sub(self, dec_val: int) -> int:
        """
        Substitute a decimal value to another one

        Args:
            dec_val (int): input

        Returns:
            int: output
        """
        return self.values[dec_val]


class SubLayer:
    """
    A susbtitution layer
    """

    def __init__(self, *sboxes):
        l = 0
        for sbox in sboxes:
            l += sbox.length
        self.length = l
        self.sboxes = list(sboxes)

    def substitute(self, bit_val: str) -> str:
        """
        Substitue a bit string to an another value

        Args:
            bit_val (str): input

        Returns:
            str: output
        """
        sections = np.array_split(list(bit_val), 4)
        new_bits = []
        for index, section in enumerate(sections):
            bits4 = "".join(section)
            old_dec = _dec(bits4)
            new_dec = self.sboxes[index].sub(old_dec)
            new_bits.append(_bin(new_dec, 4))
        return "".join(new_bits)


class TranLayer:
    """
    A transposition layer
    """

    def __init__(self, *values):
        self.values = list(values)
        self.length = len(values)

    def transpose(self, bit_val: str) -> str:
        """
        Transpose a bit string to an another value

        Args:
            bit_val (str): input

        Returns:
            str: output
        """
        output = [None] * self.length
        for index, val in enumerate(bit_val):
            output[self.values[index]] = val
        return "".join(output)


class SubKey:
    """
    A private key to be use in a SPN
    """

    def __init__(self, key):
        self.key = key
        self.length = len(key)

    def xor(self, bit_val: str) -> str:
        """
        Subkey mixing with a bit string using xor operator

        Args:
            bit_val (str): input

        Returns:
            str: output
        """
        output = [None] * self.length
        for i in range(self.length):
            output[i] = int(self.key[i]) ^ int(bit_val[i])
        return "".join(str(bit) for bit in output)


class SPN:
    """
    A substitution-permutation network
    """

    def __init__(self, sub_layer, tran_layer, keys):
        self.sub_layer = sub_layer
        self.tran_layer = tran_layer
        self.keys = keys
        self.rounds = len(keys) - 1

    def encrypt(self, plaintext: str) -> str:
        """
        Encryption loop

        Args:
            plaintext (str): original bit text

        Returns:
            str: encrypted bit text (ciphertext)
        """
        ciphertext = plaintext
        for index, key in enumerate(self.keys):
            ciphertext = key.xor(ciphertext)
            if index == self.rounds:
                return ciphertext
            ciphertext = self.sub_layer.substitute(ciphertext)
            if index == self.rounds - 1:
                continue
            ciphertext = self.tran_layer.transpose(ciphertext)


S = SBox_4(10, 2, 4, 9, 0, 14, 15, 1, 7, 6, 3, 13, 11, 8, 12, 5)
sub = SubLayer(S, S, S, S)
tran = TranLayer(0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15)
k1 = SubKey("1001010110111101")
k2 = SubKey("0011100000011111")
k3 = SubKey("0011101001110000")
k4 = SubKey("0011011001100010")
k5 = SubKey("1011101100111001")

spn = SPN(sub, tran, [k1, k2, k3, k4, k5])
msg = spn.encrypt("0000111100001111")
print(msg)
