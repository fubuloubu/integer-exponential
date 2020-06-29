@public
@constant
def evm_exp_uint256(a: uint256, b: uint256) -> uint256:
    return a ** b

@public
@constant
def exp_uint256(a: uint256, b: uint256) -> uint256:
    if a < 2 or b < 2:
        # Default to EVM in these special cases
        return a ** b  # dev: Vyper Would Revert

    x: uint256 = a
    n: uint256 = b
    y: uint256 = 1

    # NOTE: Do this at most 8 times... e.g. log_2(256)

    # 1/8
    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 2/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 3/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 4/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 5/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 6/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 7/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 8/8
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    assert n <= 1, UNREACHABLE  # Should never hit this

    return x * y


@public
@constant
def evm_exp_int128(a: int128, b: int128) -> int128:
    return a ** b

@public
@constant
def exp_int128(a: int128, b: int128) -> int128:
    assert b >= 0  # dev: SafeMath Check

    if -2 < a and a < 2 or b < 2:
        # Default to EVM in these special cases
        return a ** b  # dev: Vyper Would Revert

    assert b < 128  # dev: SafeMath Check

    x: int128 = a
    n: int128 = b
    y: int128 = 1

    # NOTE: Do this at most 7 times... e.g. log_2(128)

    # 1/7
    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 2/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 3/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 4/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 5/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 6/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    # 7/7
    if n <= 1:
        return x * y

    if n % 2 == 0:
        x *= x
        n /= 2
    else:
        y *= x
        x *= x
        n -= 1
        n /= 2

    assert n <= 1, UNREACHABLE  # Should never hit this

    return x * y
