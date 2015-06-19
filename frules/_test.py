# -*- coding: utf-8 -*-
import pytest

from frules import expressions
from frules import rules
from frules import errors


class TestVariablesHelpers:
    def test_rtrapezoid(self):
        rt = expressions.rtrapezoid(10, 20)
        assert rt(2) == 0.
        assert rt(10) == 0.
        assert rt(15) == 0.5
        assert rt(20) == 1.
        assert rt(1000) == 1.

    def test_ltrapezoid(self):
        lt = expressions.ltrapezoid(10, 20)
        assert lt(2) == 1.
        assert lt(10) == 1.
        assert lt(15) == 0.5
        assert lt(20) == 0.
        assert lt(1000) == 0.

    def test_trapezoid(self):
        tr = expressions.trapezoid(10, 20, 30, 40)

        assert tr(0) == 0.
        assert tr(10) == 0.
        assert tr(15) == 0.5
        assert tr(20) == 1.
        assert tr(25) == 1.
        assert tr(30) == 1.
        assert tr(35) == 0.5
        assert tr(40) == 0.
        assert tr(50) == 0.

    def test_triangle(self):
        tr = expressions.triangle(10, 30)

        assert tr(0) == 0.
        assert tr(10) == 0.
        assert tr(15) == 0.5
        assert tr(20) == 1.
        assert tr(25) == 0.5
        assert tr(30) == 0.
        assert tr(40) == 0.

    def test_rect(self):
        rt = expressions.rectangle(3, 5)
        assert rt(0) == 0.
        assert rt(2) == 0.
        assert rt(3) == 1.
        assert rt(4) == 1.
        assert rt(5) == 1.
        assert rt(6) == 0.

    def test_step(self):
        rt = expressions.step(3)
        assert rt(0) == 0.
        assert rt(2) == 0.
        assert rt(4) == 1.
        assert rt(5) == 1.

    def test_nstep(self):
        rt = expressions.nstep(3)
        assert rt(0) == 1.
        assert rt(2) == 1.
        assert rt(4) == 0.
        assert rt(5) == 0.
        assert rt(6) == 0.


class TestVariable:
    def test_simple_init(self):
        mu_fun = expressions.triangle(10, 30)
        var = expressions.Expression(mu_fun)

        assert var.mu(0) == 0.
        assert var.mu(10) == 0.
        assert var.mu(15) == 0.5
        assert var.mu(20) == 1.
        assert var.mu(25) == 0.5
        assert var.mu(30) == 0.
        assert var.mu(40) == 0.

    def test___str__(self):
        mu_fun = expressions.triangle(10, 30)
        var = expressions.Expression(mu_fun)

        assert isinstance(str(var), str)

    def test_variable_and(self):
        var = (
            expressions.Expression(expressions.triangle(10, 30)) &
            expressions.Expression(expressions.triangle(20, 40))
        )

        assert var.mu(0) == 0
        assert var.mu(50) == 0
        assert var.mu(20) == 0
        assert var.mu(30) == 0
        assert var.mu(25) == 0.5

    def test_variable_or(self):
        var = (
            expressions.Expression(expressions.triangle(10, 30)) |
            expressions.Expression(expressions.triangle(20, 40))
        )

        assert var.mu(0) == 0
        assert var.mu(50) == 0
        assert var.mu(20) == 1.
        assert var.mu(30) == 1.
        assert var.mu(25) == 0.5

    def test_variable_neg(self):
        var = - expressions.Expression(expressions.triangle(10, 30))
        assert var.mu(0) == 1.
        assert var.mu(10) == 1.
        assert var.mu(15) == 0.5
        assert var.mu(20) == 0.
        assert var.mu(25) == 0.5
        assert var.mu(30) == 1.
        assert var.mu(40) == 1.


class TestRule:
    def test_simple_init(self):
        V = expressions.Expression
        tall = V(expressions.rtrapezoid(170, 190), "tall")
        rules.Rule(height=tall)

    def test_rule_eval(self):
        V = expressions.Expression
        tall = V(expressions.rtrapezoid(170, 190), "tall")
        rule = rules.Rule(height=tall)

        assert rule.eval(height=100) == 0.
        assert rule.eval(height=170) == 0.
        assert rule.eval(height=180) == 0.5
        assert rule.eval(height=190) == 1.

    def test_rule_and(self):
        V = expressions.Expression
        # mu(170) == 0.  mu(180) == 0.5  mu(190) == 1.
        tall = V(expressions.rtrapezoid(170, 190), "tall")
        # mu(60) == 0.   mu(70) == 0.5.  mu(80) == 1.
        old = V(expressions.rtrapezoid(60, 80), "old")

        implicit_and = rules.Rule(height=tall, age=old)
        explicit_and = rules.Rule(height=tall) & rules.Rule(age=old)

        # min(0., 0.) == 0.
        assert (
            explicit_and.eval(height=170, age=60) ==
            implicit_and.eval(height=170, age=60) == 0.
        )

        # min(0., 0.5) == 0.
        assert (
            explicit_and.eval(height=170, age=70) ==
            implicit_and.eval(height=170, age=70) == 0.
        )

        # min(0.5, 0.5) == 0.5
        assert (
            explicit_and.eval(height=180, age=70) ==
            implicit_and.eval(height=180, age=70) == 0.5
        )

        # min(1., 0.5) == 0.5
        assert (
            explicit_and.eval(height=190, age=70) ==
            implicit_and.eval(height=190, age=70) == 0.5
        )

        # min(1., 1.) == 1.
        assert (
            explicit_and.eval(height=190, age=80) ==
            implicit_and.eval(height=190, age=80) == 1.
        )

    def test_rule_or(self):
        V = expressions.Expression
        # mu(170) == 0.  mu(180) == 0.5  mu(190) == 1.
        tall = V(expressions.rtrapezoid(170, 190), "tall")
        # mu(60) == 0.   mu(70) == 0.5.  mu(80) == 1.
        old = V(expressions.rtrapezoid(60, 80), "old")

        # from De Morgan's laws
        implicit_or = -rules.Rule(height=-tall, age=-old)
        explicit_or = rules.Rule(height=tall) | rules.Rule(age=old)

        # max(0., 0.) == 0.
        assert (
            explicit_or.eval(height=170, age=60) ==
            implicit_or.eval(height=170, age=60) == 0.
        )

        # max(0., 0.5) == 0.5
        assert (
            explicit_or.eval(height=170, age=70) ==
            implicit_or.eval(height=170, age=70) == 0.5
        )

        # max(0.5, 0.5) == 0.5
        assert (
            explicit_or.eval(height=180, age=70) ==
            implicit_or.eval(height=180, age=70) == 0.5
        )

        # max(1., 0.5) == 1.
        assert (
            explicit_or.eval(height=190, age=70) ==
            implicit_or.eval(height=190, age=70) == 1.
        )

        # max(1., 1.) == 1.
        assert (
            explicit_or.eval(height=190, age=80) ==
            implicit_or.eval(height=190, age=80) == 1.
        )

    def test_rule_neg(self):
        V = expressions.Expression
        # mu(170) == 0.  mu(180) == 0.5  mu(190) == 1.
        tall = V(expressions.rtrapezoid(170, 190), "tall")

        rule_not_tall = -rules.Rule(height=tall)
        assert rule_not_tall.eval(height=150) == 1.
        assert rule_not_tall.eval(height=170) == 1.
        assert rule_not_tall.eval(height=180) == 0.5
        assert rule_not_tall.eval(height=190) == 0.

    def test___str__(self):
        rule = rules.Rule()
        assert isinstance(str(rule), str)

    def test_eval_exception_when_input_key_missing(self):
        V = expressions.Expression
        tall = V(expressions.rtrapezoid(170, 190), "tall")
        tall_rule = rules.Rule(height=tall)
        with pytest.raises(errors.InputKeyMissing):
            tall_rule.eval(age=13)

        with pytest.raises(errors.InputKeyMissing):
            tall_rule.eval()


class TestNorms:
    pass
