"""
Simple stream ciphers implementation (only encryption at the moment)
"""


from string import ascii_uppercase

ALPHA = [*ascii_uppercase]


def xor(text1: str, text2: str) -> str:
    """
    binary xor

    Args:
        text1 (str): first binary
        text2 (str): second binary

    Returns:
        str: XORed binary
    """
    assert len(text1) == len(text2)
    value = int(text1, 2) ^ int(text2, 2)
    value = str(format(value, "b"))
    if len(value) != len(text1):
        value = "0" * (len(text1) - len(value)) + value
    return value


def caesar(plaintext: str, shift: int) -> str:
    """
    Caesar cipher implementation

    Args:
        plaintext (str): message
        shift (int): number of shift to do for each letter

    Returns:
        str: ciphertext
    """
    ciphertext = ""
    for old_letter in plaintext.upper():
        old_index = ALPHA.index(old_letter)
        new_index = (old_index + shift) % len(ALPHA)
        new_letter = ALPHA[new_index]
        ciphertext += new_letter
    return ciphertext


def vigenere(plaintext: str, shift: str) -> str:
    """
    Vigenere cipher implementation

    Args:
        plaintext (str): message
        shift (str): key string of shift

    Returns:
        str: ciphertext
    """
    ciphertext = ""
    for position, old_letter in enumerate(plaintext.upper()):
        old_index = ALPHA.index(old_letter)
        shift_index = ALPHA.index(shift.upper()[position % len(shift)])
        new_index = (old_index + shift_index) % len(ALPHA)
        new_letter = ALPHA[new_index]
        ciphertext += new_letter
    return ciphertext
