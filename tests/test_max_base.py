import pytest
import itertools

from int_exp import max_base


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
