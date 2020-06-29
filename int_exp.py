from decimal import Decimal, DivisionByZero, InvalidOperation, getcontext
import math

# Necessary to ensure we have enough precision to do the log/exp calcs
getcontext().prec = 42


def max_exp(a: int, num_bits: int, signed: bool) -> int:
    if not (num_bits % 8 == 0):
        raise ValueError("Type is not a modulo of 8")

    value_bits = num_bits - (1 if signed else 0)
    if a >= 2 ** value_bits:
        raise ValueError("Value is too large and will always throw")
    elif a < -(2 ** value_bits):
        raise ValueError("Value is too small and will always throw")

    try:
        b = int(Decimal(value_bits) / (Decimal(a).ln() / Decimal(2).ln()))
    except (DivisionByZero, InvalidOperation):
        return 1
    if b <= 1:
        return 1  # Value is assumed to be in range, therefore power of 1 is max
    # Do a bit of iteration to ensure we have the exact number
    while a ** (b + 1) < 2 ** value_bits:
        b += 1
    while a ** b >= 2 ** value_bits:
        b -= 1
    return b  # Exact


def max_base(b: int, num_bits: int, signed: bool) -> int:
    """
    For a given base `b`, compute the maximum value `a` can be
    to not produce an overflow in the equation `a ** b`
    """
    if b < 0:
        raise ValueError("Value is negative, which we cannot handle")
    elif not (num_bits % 8 == 0):
        raise ValueError("Type is not a modulo of 8")

    value_bits = num_bits - (1 if signed else 0)
    if b > value_bits:
        raise ValueError("Value is too large and will always throw")
    elif b < 2:
        return 2 ** value_bits - 1  # Maximum value for type
    else:
        # Estimate (up to ~39 digits precision required)
        a = math.ceil(2 ** (Decimal(value_bits) / Decimal(b)))
        # Do a bit of iteration to ensure we have the exact number
        while (a + 1) ** b < 2 ** value_bits:
            a += 1
        while a ** b >= 2 ** value_bits:
            a -= 1
        return a  # Exact
