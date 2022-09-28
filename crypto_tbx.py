from arithmetic import NumeralArithmetic, PolynomialArithmetic
from finite_field import FiniteField
from utils import is_prime, phi, prime_factors, primitive_roots

FIELD = 2
DIVISOR = [1, 0, 1, 1]
DIVIDEND = [1, 1, 0, 1, 1]

# PolynomialArithmetic.div_pipeline(FIELD, DIVIDEND, DIVISOR)


result = PolynomialArithmetic.multiply(FIELD, [1, 1, 0], [1, 1, 1])
print(result)
PolynomialArithmetic.div_pipeline(FIELD, result, [1, 1, 0, 1], calc_gcd=False)


print(phi(91))
