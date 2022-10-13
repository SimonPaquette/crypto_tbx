from string import ascii_uppercase
from sage.crypto.sbox import SBox

ALPHA = [*ascii_uppercase]


def xor(text1: str, text2: str) -> str:
    assert len(text1) == len(text2)
    value = int(text1, 2) ^ int(text2, 2)
    value = str(format(value, "b"))
    if len(value) != len(text1):
        value = "0" * (len(text1) - len(value)) + value
    return value


def caesar(plaintext: str, shift: int) -> str:
    ciphertext = ""
    for old_letter in plaintext.upper():
        old_index = ALPHA.index(old_letter)
        new_index = (old_index + shift) % len(ALPHA)
        new_letter = ALPHA[new_index]
        ciphertext += new_letter
    return ciphertext


def vigenere(plaintext: str, shift: str) -> str:
    ciphertext = ""
    for position, old_letter in enumerate(plaintext.upper()):
        old_index = ALPHA.index(old_letter)
        shift_index = ALPHA.index(shift.upper()[position % len(shift)])
        new_index = (old_index + shift_index) % len(ALPHA)
        new_letter = ALPHA[new_index]
        ciphertext += new_letter
    return ciphertext


"""
! check sagemath for sbox analysis
from sage.crypto.sbox import SBox
S = SBox(10,2,4,9,0,14,15,1,7,6,3,13,11,8,12,5)
S.linear_approximation_table()
S.difference_distribution_table()

"""
