from brownie.test import given
from hypothesis import example, strategies as st, settings
import pytest
import itertools

from int_exp import max_base, max_exp


@pytest.mark.parametrize("b", range(-1, 257))
@pytest.mark.parametrize("signed", [True, False])
@pytest.mark.parametrize("num_bits", range(8, 257, 8))
@pytest.mark.timeout(1)  # Ensure this computes fast in all cases
def test_max_base(b, num_bits, signed):
    if b < 0 or b > num_bits - int(signed):
        with pytest.raises(ValueError):
            max_base(b, num_bits, signed)
    elif b < 2:
        a = max_base(b, num_bits, signed)
        assert a == 2 ** (num_bits - int(signed)) - 1
    else:
        a = max_base(b, num_bits, signed)
        assert a ** b < 2 ** (num_bits - int(signed))
        assert (a + 1) ** b >= 2 ** (num_bits - int(signed))


@given(a=st.integers(min_value=-(2 ** 127), max_value=2 ** 256 - 1))
@example(a=0)
# 8 bits
@example(a=-(2 ** 7))
@example(a=-(2 ** 7) - 1)
@example(a=2 ** 7)
@example(a=2 ** 7 - 1)
# 16 bits
@example(a=-(2 ** 15))
@example(a=-(2 ** 15) - 1)
@example(a=2 ** 15)
@example(a=2 ** 15 - 1)
# 32 bits
@example(a=-(2 ** 31))
@example(a=-(2 ** 31) - 1)
@example(a=2 ** 31)
@example(a=2 ** 31 - 1)
# 64 bits
@example(a=-(2 ** 63))
@example(a=-(2 ** 63) - 1)
@example(a=2 ** 63)
@example(a=2 ** 63 - 1)
# 128 bits
@example(a=-(2 ** 127))
@example(a=-(2 ** 127) - 1)
@example(a=2 ** 127)
@example(a=2 ** 127 - 1)
# 256 bits
@example(a=2 ** 256)
@example(a=2 ** 256 - 1)
@settings(max_examples=200)  # per parametrized run
@pytest.mark.parametrize("signed", [True, False])
@pytest.mark.parametrize("num_bits", range(8, 257, 8))
def test_max_exp(a, num_bits, signed):
    if a < -(2 ** (num_bits - int(signed))) or a >= 2 ** (num_bits - int(signed)):
        with pytest.raises(ValueError):
            max_exp(a, num_bits, signed)
    else:
        b = max_exp(a, num_bits, signed)
        assert (
            # No underflow for chosen value
            a ** b >= -(2 ** (num_bits - int(signed)))
            # No overflow for chosen value
            and a ** b < 2 ** (num_bits - int(signed))
        )
        if b > 1:
            assert (
                # Either underflows
                a ** (b + 1) < -(2 ** (num_bits - int(signed)))
                # Or overflows for next value
                or a ** (b + 1) >= 2 ** (num_bits - int(signed))
            )
