# Implementation of overflow-safe version of exponentiation
# Prototyped for the EVM environment of Vyper
# from https://en.wikipedia.org/wiki/Exponentiation_by_squaring
import math
import pytest

import brownie
from hypothesis import strategies as st, settings


@pytest.fixture(scope="session")
def exp(accounts, Exp):
    yield Exp.deploy({"from": accounts[0]})


# Adapt base strategy to be reasonable with given value of power_st produces
# NOTE: Still allow some overflow/underflow cases, but make it more balanced
@st.composite
def int128_base_and_power(
    draw, n=st.integers(min_value=0, max_value=128)  # noqa: B008
):
    n = draw(n)
    x = draw(
        st.integers(
            # pulls in-range number >50% of the time (50% + 2 / 129 chance)
            min_value=-round(2 * (n ** (math.log(2 ** 127, n) / n)))
            if n > 1
            else -(2 ** 127),
            # pulls in-range number >50% of the time (50% + 2 / 129 chance)
            max_value=round(2 * (n ** (math.log(2 ** 127, n) / n)))
            if n > 1
            else 2 ** 127 - 1,
        )  # pulls in-range number >50% * >50%  = >25% of the time
    )
    return (x, n)


@brownie.test.given(xn=int128_base_and_power())
@settings(max_examples=10000)
def test_int128_power(xn, exp):
    x, n = xn
    if x ** n < -(2 ** 127) or x ** n >= 2 ** 127:
        try:
            with brownie.reverts("dev: SafeMath Check"):
                exp.exp_int128(x, n)
        except AssertionError:
            with brownie.reverts("Integer overflow"):
                exp.exp_int128(x, n)

    else:
        # Verify original operation is the same
        assert exp.evm_exp_int128(x, n) == (
            (1 if x == 0 and n == 0 else 0) if x == 0 else x ** n
        )
        assert exp.exp_int128(x, n) == (
            (1 if x == 0 and n == 0 else 0) if x == 0 else x ** n
        )


@st.composite
def uint256_base_and_power(
    draw, n=st.integers(min_value=0, max_value=256)  # noqa: B008
):
    n = draw(n)
    x = draw(
        st.integers(
            # pulls in-range number 100% of the time
            min_value=0,
            # pulls in-range number >25% of the time (25% + 2 / 257 chance)
            max_value=round(4 * (n ** (math.log(2 ** 256, n) / n)))
            if n > 1
            else 2 ** 256 - 1,
        )  # pulls in-range number 100% * >25%  = >25% of the time
    )
    return (x, n)


@brownie.test.given(xn=uint256_base_and_power())
@settings(max_examples=10000)
def test_uint256_power(xn, exp):
    x, n = xn

    # TODO: Vyper implements some SafeMath-type check on uint256 only?
    if x < 2 and n > 1:
        try:
            print("Vyper didn't revert! Result:", exp.evm_exp_uint256(x, n))
        except brownie.exceptions.VirtualMachineError:
            pass  # Try it in case it *doesn't* revert
        with brownie.reverts("Integer overflow"):
            exp.exp_uint256(x, n)

        # Also check that unchecked operation reverts
        with brownie.reverts():
            exp.evm_exp_uint256(x, n)

    elif x ** n >= 2 ** 256:
        try:
            with brownie.reverts("dev: SafeMath Check"):
                exp.exp_uint256(x, n)
        except AssertionError:
            with brownie.reverts("Integer overflow"):
                exp.exp_uint256(x, n)

    else:
        # Verify original operation is the same
        assert exp.evm_exp_uint256(x, n) == ((1 if n == 0 else 0) if x == 0 else x ** n)
        assert exp.exp_uint256(x, n) == ((1 if n == 0 else 0) if x == 0 else x ** n)
