"""
Cryptography using SPN cipher
Able to encryt a binary message with tools like Sboxes, Substition layers and Transposition layers.
"""
import json
from random import randint

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

    def __repr__(self):
        return self.key

    def __str__(self):
        return self.key

    def __getitem__(self, index):
        return self.key[index]

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

reverse_sbox = SBox_4(4, 7, 1, 10, 2, 15, 9, 8, 13, 3, 0, 12, 14, 11, 5, 6)
reverse_layer = SubLayer(reverse_sbox, reverse_sbox, reverse_sbox, reverse_sbox)


def extract_key_bits(
    n_plaintexts: int, n_bits: int, deltaP_bits: str, deltaU_bits: str, output_name: str
):

    prob = {}
    for i in range(2**n_bits):
        prob[i] = 0

    for i in range(n_plaintexts):

        deltaP = SubKey(deltaP_bits)
        deltaU = SubKey(deltaU_bits)

        plain1 = _bin(i, 16)
        plain2 = deltaP.xor(plain1)

        cipher1 = spn.encrypt(plain1)
        cipher2 = spn.encrypt(plain2)

        for integer in range(2**n_bits):
            bin_integer = _bin(integer, 16)
            index_to_compare_with = []

            random_key = ""
            for split in range(0, 16, 4):
                if "1" in deltaU[split : split + 4]:
                    random_key += bin_integer[split : split + 4]
                    index_to_compare_with.extend(range(split, split + 4))
                else:
                    random_key += "0000"
            random_key = SubKey(random_key)

            c1_xor = random_key.xor(cipher1)
            c2_xor = random_key.xor(cipher2)

            c1_sub = reverse_layer.substitute(c1_xor)
            c2_sub = reverse_layer.substitute(c2_xor)

            right_pair = True
            for index, diff_bit in enumerate(deltaU):
                if index in index_to_compare_with:
                    if diff_bit == "1":
                        if c1_sub[index] == c2_sub[index]:
                            right_pair = False
                            break
                    else:
                        if c1_sub[index] != c2_sub[index]:
                            right_pair = False
                            break

            if right_pair:
                prob[integer] += 1

    max_value = 0
    index = None
    with open(f"{output_name}.txt", "w") as f:
        for k, v in prob.items():
            v = v / n_plaintexts
            k = _bin(k, n_bits)

            keys = [k[i : i + 4] for i in range(0, len(k), 4)]

            f.write(f"{keys} : {v:.4f}\n")

            if v > max_value:
                max_value = v
                index = k

    print(index, max_value)


extract_key_bits(5000, 8, "0001000000000000", "0000000001000100", "diff_car_1")
