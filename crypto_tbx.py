import math

from arithmetic import NumeralArithmetic, PolynomialArithmetic
from cipher import caesar, vigenere, xor
from finite_field import FiniteField
from PRNG import BBS, LCG
from utils import (
    discrete_log,
    is_prime,
    n_test_miller_rabin,
    phi,
    prime_factors,
    primitive_roots,
)

#!##################################################################
#! FINITE FIELD
#!##################################################################

# ELEMS = [1, 2, 3, 4]
# MOD = 5

# ff = FiniteField(ELEMS, MOD)
# print(ff.is_group())
# print(ff.is_abelian_group())
# print(ff.is_ring())
# print(ff.is_commutative_ring())
# print(ff.is_integral_domain())
# print(ff.is_field())


#!##################################################################
#! Arithmetic
#!##################################################################

# ? Function
# print(is_prime(11))
# print(prime_factors(30))
# print(math.gcd(3, 6))
# print(phi(91))
# print(n_test_miller_rabin(500))
# print(discrete_log(2, 13, 17))

# ? Polynomial operator
# FIELD = 2
# POLY1 = [1, 0, 1]
# POLY2 = [1, 1, 0]
# print(PolynomialArithmetic.add(FIELD, POLY1, POLY2))
# print(PolynomialArithmetic.substract(FIELD, POLY1, POLY2))
# print(PolynomialArithmetic.multiply(FIELD, POLY1, POLY2))
# print(PolynomialArithmetic.multiply_by_int(FIELD, POLY1, 4))

# print(PolynomialArithmetic.mod_irreducible([1, 1, 1, 1, 0], [1, 1, 0, 1]))

# ? Polynomial division and gcd
# FIELD = 101
# POLY1 = [1, 88, 73, 83, 51, 67]
# POLY2 = [1, 97, 40, 38]
# PolynomialArithmetic.div_pipeline(FIELD, POLY1, POLY2)

# ? Inverse
# print(NumeralArithmetic.find_inverse(1234, 4231))

# ? Chinese remainder
# NumeralArithmetic.chinese_remainder(2431)
# print(NumeralArithmetic.to_tuple_repr(30, 19))
# a = NumeralArithmetic.to_tuple_repr(2431, 1813)
# print(NumeralArithmetic.from_tuple_repr(30, [0, 2, 4]))

# ? Primitive roots
# primitive_roots(25)


#!##################################################################
#! Cipher
#!##################################################################

# ? Simple
# print(xor("1010", "1100"))
# print(caesar("hellojohn", 3))
# print(vigenere("hellojohn", "vig"))

# ? SPN - Sbox - linear - differential
# * check ldc_tut.py for SPN implementation
# * use sagemath for sbox analysis
# from sage.crypto.sbox import SBox
# S = SBox(10,2,4,9,0,14,15,1,7,6,3,13,11,8,12,5)
# S.linear_approximation_table()
# S.difference_distribution_table()


#!##################################################################
#! PRNG
#!##################################################################

# ? Blum Blum Shub
# blum = BBS(911 * 991, 613)
# blum.generate(10)

# ? Linear Congruential Generator
# gen = LCG(7, 0, 32, 5)
# gen.generate(10)
