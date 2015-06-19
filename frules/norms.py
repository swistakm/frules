# -*- coding: utf-8 -*-
from functools import reduce


# MIN, MAX norms
def _AND_MAX(funcs, *args, **kwargs):
    return min([func(*args, **kwargs) for func in funcs])


def _OR_MIN(funcs, *args, **kwargs):
    return max([func(*args, **kwargs) for func in funcs])


# PROD, SUM norms
def _AND_PROD(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b: val_a * val_b,
        [fun(*args, **kwargs) for fun in funcs]
    )


def _OR_SUM(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b: val_a + val_b - val_a * val_b,
        [fun(*args, **kwargs) for fun in funcs]
    )


# HAMACHER norms
def _AND_HAMACHER(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b: (val_a * val_b) / (val_a + val_b - val_a * val_b),
        [fun(*args, **kwargs) for fun in funcs]
    )


def _OR_HAMACHER(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b:
            (val_a + val_b - 2 * val_a * val_b) / (1 - val_a * val_b),
        [fun(*args, **kwargs) for fun in funcs]
    )


# EINSTEIN norms
def _AND_EINSTEIN(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b:
            (val_a * val_b) / (2 - (val_a + val_b - val_a * val_b)),
        [fun(*args, **kwargs) for fun in funcs]
    )


def _OR_EINSTEIN(funcs, *args, **kwargs):
    return reduce(
        lambda val_a, val_b: (val_a + val_b) / (1 + val_a * val_b),
        [fun(*args, **kwargs) for fun in funcs]
    )


def neg_norm(func, *args, **kwargs):
    assert len(func) == 1
    return 1.0 - func[0](*args, **kwargs)


def and_norm(funcs, *args, **kwargs):
    return DEFAULT_NORM_SET[0](funcs, *args, **kwargs)


def or_norm(funcs, *args, **kwargs):
    return DEFAULT_NORM_SET[1](funcs, *args, **kwargs)


MAX_MIN_NORM_SET = (_AND_MAX, _OR_MIN)
PROD_SUM_NORM_SET = (_AND_PROD, _OR_SUM)
HAMACHER_NORM_SET = (_AND_HAMACHER, _OR_HAMACHER)
EINSTEIN_NORM_SET = (_AND_EINSTEIN, _OR_EINSTEIN)

DEFAULT_NORM_SET = MAX_MIN_NORM_SET
