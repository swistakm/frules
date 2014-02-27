# -*- coding: utf-8 -*-
class BaseFuzzyException(BaseException):
    """ Base exception for fuzzy module"""


class InputKeyMissing(BaseFuzzyException):
    """Raised when insufficient input data specified"""


class AmbiguousRuleDefinitionError(BaseException):
    """Raised when Rule definition is Ambiguous"""
