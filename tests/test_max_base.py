import pytest
import itertools

from int_exp import max_base


@pytest.mark.parametrize("b", range(-1, 257))
@pytest.mark.parametrize("signed", [True, False])
@pytest.mark.parametrize("bits", range(8, 257, 8))
@pytest.mark.timeout(1)  # Ensure this computes fast in all cases
def test_max_base(b, signed, bits):
    typ = f"{'u' if signed else ''}int{bits}"
    if b > bits - int(signed):
        with pytest.raises(ValueError):
            a = max_base(b, typ=typ)
    elif b < 2:
        a = max_base(b, typ=typ)
        assert a == 2 ** (bits - int(signed)) - 1
    else:
        a = max_base(b, typ=typ)
        assert a ** b < 2 ** (bits - int(signed))
        assert (a + 1) ** b >= 2 ** (bits - int(signed))
