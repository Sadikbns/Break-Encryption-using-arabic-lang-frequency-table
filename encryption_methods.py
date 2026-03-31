# 2 - This file contains the 3 encryption methods (cesar - affine - substitution) + their decryption methods

import random
import math

# 2.0 - define arabic alphabet arrays name arabic_alphabet
arabic_alphabet = [
    'ا', 'أ', 'إ', 'آ', 'ء',
    'ب', 'ت', 'ث', 'ج', 'ح', 'خ',
    'د', 'ذ', 'ر', 'ز',
    'س', 'ش', 'ص', 'ض', 'ط', 'ظ',
    'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
    'م', 'ن', 'ه', 'و', 'ي',
    'ة', 'ى', 'ئ', 'ؤ',
]

N = len(arabic_alphabet)  # alphabet size (36)
char_to_idx = {ch: i for i, ch in enumerate(arabic_alphabet)}


# 2.1 - cesar encryption / decryption functions

def cesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Shifts each Arabic letter forward by `shift` positions (mod N).
    Non-alphabet characters (spaces, punctuation, digits) are left unchanged.
    """
    result = []
    for ch in plaintext:
        if ch in char_to_idx:
            result.append(arabic_alphabet[(char_to_idx[ch] + shift) % N])
        else:
            result.append(ch)
    return ''.join(result)


def cesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    Reverses Caesar encryption by shifting backward by `shift` positions.
    """
    return cesar_encrypt(ciphertext, -shift)


# 2.2 - affine encryption / decryption functions

def _mod_inverse(a: int, m: int) -> int:
    """Returns the modular inverse of a under mod m using extended Euclidean algorithm."""
    if math.gcd(a, m) != 1:
        raise ValueError(f"'a'={a} has no modular inverse mod {m}. gcd must be 1.")
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"No modular inverse found for a={a}, m={m}")


def affine_encrypt(plaintext: str, a: int, b: int) -> str:
    """
    Encrypts using the affine cipher: E(x) = (a*x + b) mod N.
    `a` must be coprime with N (alphabet size).
    Non-alphabet characters are left unchanged.
    """
    if math.gcd(a, N) != 1:
        raise ValueError(f"'a'={a} must be coprime with alphabet size N={N}")
    result = []
    for ch in plaintext:
        if ch in char_to_idx:
            result.append(arabic_alphabet[(a * char_to_idx[ch] + b) % N])
        else:
            result.append(ch)
    return ''.join(result)


def affine_decrypt(ciphertext: str, a: int, b: int) -> str:
    """
    Decrypts an affine cipher: D(y) = a_inv * (y - b) mod N.
    """
    if math.gcd(a, N) != 1:
        raise ValueError(f"'a'={a} must be coprime with alphabet size N={N}")
    a_inv = _mod_inverse(a, N)
    result = []
    for ch in ciphertext:
        if ch in char_to_idx:
            result.append(arabic_alphabet[(a_inv * (char_to_idx[ch] - b)) % N])
        else:
            result.append(ch)
    return ''.join(result)


# 2.3 - substitution encryption / decryption functions

# 2.3.1 - here we define the substitution dictionnary named arabic_substitution to be used in enc and dec like 'a' -> 'x', 'b' -> 't' ...
shuffled = arabic_alphabet.copy()
random.shuffle(shuffled)
arabic_substitution = {arabic_alphabet[i]: shuffled[i] for i in range(N)}


def substitution_encrypt(plaintext: str, substitution: dict = arabic_substitution) -> str:
    """
    Encrypts by replacing each Arabic letter using the substitution dictionary.
    Spaces, punctuation, and non-alphabet characters are left unchanged.
    """
    result = []
    for ch in plaintext:
        result.append(substitution.get(ch, ch))
    return ''.join(result)


def substitution_decrypt(ciphertext: str, substitution: dict = arabic_substitution) -> str:
    """
    Decrypts by reversing the substitution dictionary (value -> key).
    """
    reverse_sub = {v: k for k, v in substitution.items()}
    result = []
    for ch in ciphertext:
        result.append(reverse_sub.get(ch, ch))
    return ''.join(result)

