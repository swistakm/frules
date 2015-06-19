# -*- coding: utf-8 -*-
def range(start, stop, step=1.):
    """Replacement for built-in range function.

    :param start: Starting value.
    :type start: number
    :param stop: End value.
    :type stop: number
    :param step: Step size.
    :type step: number
    :returns: List of values from `start` to `stop` incremented by `size`.
    :rtype: [float]
    """
    start, stop, step = map(float, (start, stop, step))

    result = [start]
    current = start
    while current < stop:
        current += step
        result.append(current)
    return result


def up(a, b, x):
    a, b, x = map(float, (a, b, x))

    a = float(a)
    b = float(b)
    x = float(x)
    if x < a:
        return 0.0
    if x < b:
        return (x - a) / (b - a)
    return 1.0


def down(a, b, x):
    return 1. - up(a, b, x)


def tri(a, b, x):
    a, b, x = map(float, (a, b, x))

    m = (a + b) / 2.
    first = (x - a) / (m - a)
    second = (b - x) / (b - m)
    return max(min(first, second), 0.)


def trap(a, b, c, d, x):
    a, b, c, d, x = map(float, (a, b, c, d, x))

    first = (x - a) / (b - a)
    second = (d - x) / (d - c)
    return max(min(first, 1., second), 0.)


def ltrap(a, b, x):
    a, b, x = map(float, (a, b, x))
    return max(min((b - x) / (b - a), 1.), 0.)


def rtrap(a, b, x):
    a, b, x = map(float, (a, b, x))
    return max(min((x - a) / (b - a), 1.), 0.)


def rect(a, b, x):
    a, b, x = map(float, (a, b, x))
    return 1. if a < x < b else 0
