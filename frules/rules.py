# -*- coding: utf-8 -*-
from functools import reduce

from frules.errors import InputKeyMissing, AmbiguousRuleDefinitionError
from frules.expressions import Expression
from frules.norms import and_norm, or_norm, neg_norm


class Rule(object):
    _children = None
    _op = None

    def __new__(cls, input_bind=None, variable=None, **kwargs):
        """Creates new Rule instance

        If rule definition is provided in kwargs-style, each rule is
        instantiated as separate Rule object and they are
        joined with & operator.
        """
        filtered_keys = filter(
            lambda key: isinstance(kwargs[key], Expression), kwargs
        )
        rules_definitions = [(key, kwargs[key]) for key in filtered_keys]

        if (input_bind or variable) and rules_definitions:
            raise AmbiguousRuleDefinitionError(
                "Can't define Rule with both args-style and"
                " kwargs-style input bindings"
            )

        print(rules_definitions)
        if rules_definitions:
            # kwargs-style definition
            # instantiate each Rule and join them with "and" operator
            rules = [object.__new__(cls) for __ in rules_definitions]
            for rule, (bind, var) in zip(rules, rules_definitions):
                rule._pre_init(bind, var)
            return reduce(lambda a, b: a & b, rules)
        else:
            # args-style definition
            rule = object.__new__(cls)
            rule._pre_init(input_bind, variable)
            return rule

    def _pre_init(self, input_bind=None, variable=None):
        """Bind input key and variable
        """
        self._input_bind = input_bind
        self._variable = variable

    @staticmethod
    def apply_norm(children, norm, op):
        """Apply provided norm to new Rule object"""
        rule = Rule()
        rule._children = children
        rule._norm = norm
        rule._op = op
        return rule

    def __and__(self, other):
        return Rule.apply_norm(children=[self, other], norm=and_norm, op="&")

    def __or__(self, other):
        return Rule.apply_norm(children=[self, other], norm=or_norm, op="|")

    def __neg__(self):
        return Rule.apply_norm(children=[self], norm=neg_norm, op="!")

    def eval(self, **inputs):
        """Evaluate rule with specified inputs"""
        if self._input_bind:
            try:
                return self._variable.mu(inputs[self._input_bind])
            except KeyError:
                raise InputKeyMissing(self._input_bind)
        elif self._children:
            return self._norm([rule.eval for rule in self._children], **inputs)

    def __str__(self):
        """Return string representing fuzzy logic rule """
        if self._children:
            if len(self._children) > 1:
                op = " %s " % self._op
                rep = "(%s)" % op.join([str(rule) for rule in self._children])
            else:
                rep = self._op + str(self._children[0])
            return rep
        else:
            return "%s = %s" % (self._input_bind, self._variable)

    def __repr__(self):
        return str(self)
