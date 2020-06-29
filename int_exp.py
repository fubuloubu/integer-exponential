from decimal import Decimal
import math


PRECOMPUTED = {
    "uint256": {
        14: 319557,
        13: 847179,
        12: 2642245,
        11: 10134188,
        10: 50859008,
        9: 365284284,
        8: 4294967295,
        7: 102116749982,
        6: 6981463658331,
        5: 2586638741762874,
        4: 18446744073709551615,
        3: 48740834812604276470692694,
        2: 340282366920938463463374607431768211455,
    },
}


def max_base(b: int, typ: str = "uint256") -> int:
    """
    For a given base `b`, compute the maximum value `a` can be
    to not produce an overflow in the equation `a ** b`
    """
    integer_traits = typ.split("int")
    value_bits = int(integer_traits[-1]) - (1 if "u" in typ else 0)
    if not (int(integer_traits[-1]) % 8 == 0):
        raise ValueError("Type is not a modulo of 8")
    elif b > value_bits:
        raise ValueError("Value is too large and will always throw")
    elif b < 2:
        return 2 ** value_bits - 1  # Maximum value for type
    # All precomputed values computing using the below loop
    # NOTE: Precalulated these because they take so long
    elif typ in PRECOMPUTED and b in PRECOMPUTED[typ]:
        return PRECOMPUTED[typ][b]
    else:
        a = 2 ** math.ceil(Decimal(value_bits) / Decimal(b))  # Estimate
        while (a + 1) ** b < 2 ** value_bits:
            a += 1
        while a ** b >= 2 ** value_bits:
            a -= 1
        return a  # Exact
