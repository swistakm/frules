# frules - simple functional fuzzy rules


Frules stands for **fuzzy/funtional rules**. It allows to work easily with
fuzzy rules and variables.

Installation:

    pip install frules


## Linguistic variables and expressions
Expression is a core concept in frules. `Expression` class represents subrange
of [linguistic variable](http://en.wikipedia.org/wiki/Fuzzy_logic#Linguistic_variables) in
fuzzy logic.

Variables in classical math take numerical values. in fuzzy logic, the
*linguistic variables* are non-numeric and are described with expressions.
Expressions map continuous variable like nemerical temperature to its
linguistic counterpart. For example temperature can be described as cold, warm
or hot. There is no strict boundary between cold and warm - this is why this
expressions are fuzzy.

To create new expression we use function that takes numerical value of
contiunous variable and returns *truth value*. Truth value ranges between
0 and 1 - it's a degree of membership of continous value to that linguistic
variable.

```python
from frules.expressions import Expression
#We know that anything over 50 degrees is hot and below 40 is't hot
hot = Expression(lambda x: min(1, max((x - 40) / 10., 0)))
```

This ugly lambda is representation of some fuzzy set. If we take a look how it
behaves, we'll see that it in fact returns 1 for anything over 50, 0 for
anything below 40 and some linear values between 40 and 50:

```python
>>> map(lambda x: {x: min(1, max((x - 40) / 10., 0))}, xrange(35, 55, 2))
[{35: 0}, {37: 0}, {39: 0}, {41: 0.1}, {43: 0.3}, {45: 0.5}, {47: 0.7}, {49: 0.9}, {51: 1}, {53: 1}
```

Using a lot of lambdas in practice makes your code a mess. Fuzzy expressions
described this way are additionally hard to write because of some value
assertions they must satisfy.

This is why we ancapsulate don't use raw functions and encapsulate them with
expressions. Moreover frules provides a bunch of helpers that eases definition
of new expressions. Example of full set of expressions for temperature variable
could look this way:

```python
from frules.expressions import Expression as E
from frules.expressions import ltrapezoid, trapezoid, rtrapezoid

cold = E(ltrapezoid(10, 20), "cold")        # anything below 10, more is fuzzy
warm = E(trapezoid(10, 20, 30, 35), "warm") # anything between 20 and 30
hot = E(rtrapezoid(30, 35), "hot")          # anything over 35, less is fuzzy
```

Expressions can be reused/mixed using logical operators:

```python
cold_or_hot = cold || warm
not_hot = !hot
```

Optional names will be helpful when we start to work with fuzzy rules.

## Fuzzy rules
Although expressions define linguistic variables, they aren't strictly bound
to any variable. They are rather the adjectives we use to describe something and
their meaning depends strictly on context. Both *person* and *data* could
be *big* but this particular adjective has slighlty different meaning in each
case.

`Rule` objects bounds continous variable with expressions. Rules also can also
be evaluated to see how true they are for given continous input.

```
>>> from frules.rules import Rule
>>> is_hot = Rule(temperature=hot)
>>> is_hot.eval(temperature=5)
0.8
```

Rules can be mixed using logical operators (`&` and `|`) to create more
sophisticated rules that allow fuzzy reasoning:

```python
from frules.expressions import Expression as E
from frules.rules import Rule as R
from frules.expressions import ltrapezoid, trapezoid, rtrapezoid

# age expressions
too_young = E(ltrapezoid(16, 18), "too_young")
young = E(trapezoid(16, 18, 25, 30), "young")
old = - (too_young && young)

# height expressions
tall = E(rtrapezoid(165, 180), "tall")
short = E(ltrapezoid(165, 180), "short")

# yes expression
yes = E(lambda yes: float(yes), "yes") # converts bool to float


# rules
is_hot = R(age=young, height=tall)  # equvalent to R(age=young) & R(height=tall)
is_chick = - R(has_penis=yes)
should_date = is_hot & is_chick
```

Having set such rules we can do some reasoning:

```
>>> shoud_date
((age = young & height = tall) & !has_penis = yes)
>>> should_date.eval(age=17, height=170, has_penis=False) > should_date.eval(age=20, height=170, has_penis=True)
True
>>>
>>> candidates = {
...     "c1": {"age": 18, "height": 178},
...     "c2": {"age": 20, "height": 175},
...     "c3": {"age": 50, "height": 180},
...     "c4": {"age": 25, "height": 161},
... }
...
>>> max(candidates.iteritems(), key=lambda (key, inputs): is_hot.eval(**inputs))
('c1', {'age': 18, 'height': 178})
```

