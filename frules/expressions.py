# -*- coding: utf-8 -*-
from functools import partial

from frules import primitives
from frules.norms import and_norm, or_norm, neg_norm


class Expression(object):
    _children = None
    _op = None

    def __init__(self, mu_func=None, name=None):
        if callable(mu_func):
            self._mu_func = mu_func
            self._name = name

    def mu(self, val):
        if self._mu_func:
            return self._mu_func(val)

    @staticmethod
    def apply_norm(children, norm, op):
        """Apply provided norm to new Expression object"""
        mu_list = [child.mu for child in children]
        var = Expression(lambda val, children=mu_list: norm(children, val))
        var._children = children
        var._op = op
        return var

    def __and__(self, other):
        return Expression.apply_norm([self, other], and_norm, "&")

    def __or__(self, other):
        return Expression.apply_norm([self, other], or_norm, "|")

    def __neg__(self):
        return Expression.apply_norm([self], neg_norm, "!")

    def __str__(self):
        if self._children:
            if len(self._children) > 1:
                op = " %s " % self._op
                rep = "(%s)" % op.join([str(rule) for rule in self._children])
            else:
                rep = self._op + str(self._children[0])
            return rep
        elif self._name:
            return self._name
        else:
            return "undefined"


def trapezoid(a, b, c, d):
    """ Return trapezoid function:

        ^   .....
        |  /     \
        |_/_______\_
         a  b   c  d
    """
    return partial(primitives.trap, a, b, c, d)


def rtrapezoid(a, b):
    """ Return trapezoid function with right side in infinity:


        ^     ........
        |    /
        |___/_________
           a  b
    """
    return partial(primitives.rtrap, a, b)


def ltrapezoid(a, b):
    """ Return trapezoid function with left side in infinity:

        ^........
        |        \
        |_________\__
                a  b
    """
    return partial(primitives.ltrap, a, b)


def triangle(a, b):
    """ Return triangle function:

        ^      .
        |     / \
        |____/___\____
             a   b
    """
    return partial(primitives.tri, a, b)


def rectangle(a, b):
    """ Return classic logic rect function:

        ^   ......
        |   |    |
        |___|____|___
            a    b
    """
    return lambda x, a=a, b=b: 1. if a <= x <= b else 0.


def step(a):
    """ Return logic step function
        ^   .........
        |   |
        |___|________
            a
    """
    return lambda x: 1. if x > a else 0.


def nstep(a):
    """ Return negative logic step function
        ^....
        |   |
        |___|________
            a
    """
    return lambda x: 1. if x <= a else 0.
