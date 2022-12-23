"""
Public-key cryptographic implementation
"""

import math

from arithmetic import NumeralArithmetic
from utils import phi


class RSA:
    """
    Public-key RSA implementation
    """

    def __init__(
        self,
        public_key_e: int = None,
        private_key_d: int = None,
        prime_p: int = None,
        prime_q: int = None,
        pq: int = None,
    ):
        """
        algo and keys initialization

        Args:
            public_key_e (int, optional): An RSA public key. Defaults to None.
            private_key_d (int, optional): An RSA private key. Defaults to None.
            prime_p (int, optional): big integer prime p. Defaults to None.
            prime_q (int, optional): big integer prime q. Defaults to None.
            pq (int, optional): modulo n, product of p and q. Defaults to None.
        """
        self.public_key_e = public_key_e
        self.private_key_d = private_key_d
        self.prime_p = prime_p
        self.prime_q = prime_q
        self.pq = pq

        if (pq is None) and (prime_p is not None) and (prime_q is not None):
            self.pq = prime_p * prime_q

        self.phi = phi(self.pq)

    def __repr__(self) -> str:
        """
        printable representation of the RSA parameters

        Returns:
            str: RSA object parameters
        """
        return str(vars(self))

    def _valid_public_key_e(self):
        """
        Validate public key requirements
        """
        assert isinstance(self.public_key_e, int)
        assert self.public_key_e > 1
        assert self.public_key_e < self.phi
        assert math.gcd(self.public_key_e, self.phi) == 1

    def _valid_private_key_d(self):
        """
        Validate private key requirements
        """
        assert isinstance(self.private_key_d, int)
        assert self.private_key_d > 1
        assert self.private_key_d < self.phi
        assert ((self.public_key_e * self.private_key_d) % self.phi) == 1

    def _valid_pq(self):
        """
        validate modulo n requirement
        """
        assert isinstance(self.pq, int)

    def select_keys(self):
        """
        choose public and private keys if none given
        """
        assert self.public_key_e is None
        assert self.private_key_d is None

        for i in range(self.phi - 1, 1, -1):
            try:
                self.public_key_e = i
                self._valid_public_key_e()
                self.private_key_d = NumeralArithmetic.find_inverse(
                    self.public_key_e, self.phi, False
                )
                self._valid_private_key_d()
                assert self.public_key_e != self.private_key_d
                break
            except AssertionError:
                pass
            except ZeroDivisionError:
                pass

    def set_keys(self, public_key: int):
        """
        find private key that match the public key and modulo n

        Args:
            public_key (int): RSA public key
        """
        self.public_key_e = public_key
        self._valid_public_key_e()
        self.private_key_d = NumeralArithmetic.find_inverse(
            self.public_key_e, self.phi, False
        )
        self._valid_public_key_e()
        self._valid_private_key_d()

    def encrypt(self, message: int) -> int:
        """
        RSA encryption algo

        Args:
            message (int): the plaintext to encrypt

        Returns:
            int: RSA ciphertext
        """
        assert isinstance(message, int)
        assert message > 0
        assert message < self.phi
        self._valid_public_key_e()
        self._valid_pq()

        c = pow(base=message, exp=self.public_key_e, mod=self.pq)
        return c

    def decrypt(self, ciphertext: int) -> int:
        """
        RSA decryption alfo

        Args:
            ciphertext (int): RSA encrypted message

        Returns:
            int: plaintext
        """
        assert isinstance(ciphertext, int)
        self._valid_private_key_d()
        self._valid_pq()

        m = pow(base=ciphertext, exp=self.private_key_d, mod=self.pq)
        return m

    def decrypt_CRT(self, ciphertext: int) -> None:
        """
        printable steps of chinese remainder theorem

        Args:
            ciphertext (int): RSA encrypted message
        """
        vp = pow(ciphertext, self.private_key_d % (self.prime_p - 1), self.prime_p)
        vq = pow(ciphertext, self.private_key_d % (self.prime_q - 1), self.prime_q)
        xp = self.prime_q * pow(self.prime_q, -1, self.prime_p)
        xq = self.prime_p * pow(self.prime_p, -1, self.prime_q)
        plaintext = (vp * xp + vq * xq) % self.pq

        print(
            f"vp = c^(d mod p-1) mod p = {ciphertext}^({self.private_key_d} mod {self.prime_p-1}) mod {self.prime_p} = {vp}"
        )
        print(
            f"vq = c^(d mod q-1) mod q = {ciphertext}^({self.private_key_d} mod {self.prime_q-1}) mod {self.prime_q} = {vq}"
        )
        print(f"xp = q * q^-1 mod p = {xp}")
        print(f"xq = p * p^-1 mod q = {xq}")
        print(
            f"Plaintext = (vp*xp + vq*xq) mod n = ({vp}*{xp} + {vq}*{xq}) mod {self.pq} = {plaintext}"
        )


class ECurve:
    """
    (interface) of an elliptic curve cryptographic algorithm
    """

    def __init__(self, prime: int, a: int, b: int):
        """
        basic representation of EC

        Args:
            prime (int): field of the prime (mod)
            a (int): value a in the EC formula
            b (int): value b in the EC formula
        """
        self.prime = prime
        self.a = a
        self.b = b

    def is_point(self, x: int, y: int) -> bool:
        """
        function needed for each implementation, check if a point exists in this elliptic curve

        Args:
            x (int): coordinate x
            y (int): coordinate y

        Raises:
            NotImplementedError: abstract

        Returns:
            bool: point included in this EC
        """
        raise NotImplementedError

    def list_point(self) -> list[tuple[int, int]]:
        """
        List all points that exists in this EC

        Returns:
            list[tuple[int, int]]: a list of points (x,y)
        """
        points = []
        for x in range(self.prime):
            for y in range(self.prime):
                if self.is_point(x, y):
                    points.append((x, y))
        return points


class ECurve_GFP(ECurve):
    """
    ECC over galois field a prime GF(p)

    Args:
        ECurve (_type_): EC
    """

    def get_equation(self) -> str:
        """
        get equation representing the EC

        Returns:
            str: EC GF(p) formula
        """
        return f"( y^2 = x^3 + {self.a}x + {self.b} ) mod {self.prime}"

    def is_point(self, x: int, y: int) -> bool:
        """
        check if a point exists in this elliptic curve

        Args:
            x (int): coord x
            y (int): coord x

        Returns:
            bool: this point exists
        """
        left = pow(y, 2, self.prime)
        right = (x**3 + self.a * x + self.b) % self.prime
        return left == right

    def negative_point(self, x: int, y: int) -> tuple[int, int]:
        """
        get the inverse of a point

        Args:
            x (int): coord x
            y (int): coord y

        Returns:
            tuple[int, int]: inverse (negative) of a point
        """
        return (x, (-y) % self.prime)

    def double_point(self, x: int, y: int) -> tuple[int, int]:
        """
        multiply a point by itself

        Args:
            x (int): coord x
            y (int): coord y

        Returns:
            tuple[int, int]: 2P
        """
        slope = ((3 * x**2 + self.a) * (pow(2 * y, -1, self.prime))) % self.prime
        xr = (slope**2 - 2 * x) % self.prime
        yr = (slope * (x - xr) - y) % self.prime
        return (xr, yr)

    def addition(self, xp: int, yp: int, xq: int, yq: int) -> tuple[int, int]:
        """
        add two points

        Args:
            xp (int): coord x of point 1
            yp (int): coord y of point 1
            xq (int): coord x of point 2
            yq (int): coord y of point 2

        Returns:
            tuple[int, int]: sum of two points
        """
        slope = (((yq - yp) % self.prime) * (pow(xq - xp, -1, self.prime))) % self.prime
        xr = (slope**2 - xp - xq) % self.prime
        yr = (-yp + slope * (xp - xr)) % self.prime
        return (xr, yr)

    def multiplication(self, integer: int, x: int, y: int) -> tuple[int, int]:
        """
        multiply a point by itself n times

        Args:
            integer (int): n times
            x (int): coord x
            y (int): coord y

        Returns:
            tuple[int, int]: a new point
        """
        assert integer > 1
        temp_x, temp_y = self.double_point(x, y)
        for _ in range(integer - 2):
            temp_x, temp_y = self.addition(temp_x, temp_y, x, y)
        return (temp_x, temp_y)

    def substraction(self):
        raise NotImplementedError


class ECC:
    """
    Elliptic curve cryptographic implementation
    """

    def __init__(self, curve: ECurve_GFP, x: int, y: int, private_key: int):
        """
        algo and parameters initialization

        Args:
            curve (ECurve_GFP): an elliptic curve (only in GF(p) at the moment, could implement GF(2^n) later)
            x (int): a point x coordinate
            y (int): a point y coordinate
            private_key (int): an ECC private key
        """
        assert curve.is_point(x, y)
        self.curve = curve
        self.x = x
        self.y = y
        self.private_key = private_key
        self.public_key = self._set_public_key()

    def _set_public_key(self) -> tuple[int, int]:
        """
        set a ECC public key from the ECC private key

        Returns:
            tuple[int, int]: ECC public key
        """
        return self.curve.multiplication(self.private_key, self.x, self.y)

    def get_public_key(self) -> tuple[int, int]:
        """
        getter public key

        Returns:
            tuple[int, int]: ECC public key
        """
        return self.public_key

    def encrypt(self, k: int, message: tuple[int, int]) -> tuple[int, int]:
        """
        ECC encryption implementation

        Args:
            k (int): a one time key
            message (tuple[int, int]): plaintext

        Returns:
            tuple[int, int]: ciphertext
        """
        assert self.curve.is_point(message[0], message[1])
        part1 = self.curve.multiplication(k, self.x, self.y)
        part2 = self.curve.multiplication(k, self.public_key[0], self.public_key[1])
        part2 = self.curve.addition(message[0], message[1], part2[0], part2[1])
        return (part1, part2)

    def decrypt(self):
        # TODO: ECC.decrypt() need ECurve_GFP.substration()
        raise NotImplementedError


class ECurve_GF2(ECurve):
    # TODO: add function similar to class ECurve_GFP
    def get_equation(self) -> str:
        """
        get equation representing the EC

        Returns:
            str: EC GF(2^n) formula
        """
        return f"( y^2 + xy = x^3 + {self.a}x^2 + {self.b} ) mod {self.prime}"

    def is_point(self, x: int, y: int) -> bool:
        """
        check if a point exists in this elliptic curve

        Args:
            x (int): coord x
            y (int): coord x

        Returns:
            bool: this point exists
        """
        left = (y**2 + x * y) % self.prime
        right = (x**3 + self.a * x**2 + self.b) % self.prime
        return left == right


# gfp = ECurve_GFP(23, 1, 1)
# point = gfp.list_point()[3]
# ecc = ECC(gfp, point[0], point[1], 5)
# message = gfp.list_point()[8]
# cipher = ecc.encrypt(7, message)
# print(cipher)
