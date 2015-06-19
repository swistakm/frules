# -*- coding: utf-8 -*-
from functools import partial
import math


def hedge(p, mvalue):
    """Generic definition of a function that alters a given membership function
    by intensifying it in the case of *very* of diluting it in the case of
    *somewhat*.  """

    mvalue = float(mvalue)
    if not p:
        return 0.0
    return math.pow(mvalue, p)

very = partial(hedge, 2.)
extermely = partial(hedge, 3.)
somewhat = partial(hedge, 0.5)
slightly = partial(hedge, 1. / 3.)
