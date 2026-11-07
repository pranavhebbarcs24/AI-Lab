# First Order Logic - Unification Algorithm

# Check whether a term is a variable
def is_variable(x):
    return isinstance(x, str) and x[0].islower()


# Apply substitutions to a term
def substitute(term, subs):
    while isinstance(term, str) and term in subs:
        term = subs[term]
    return term


# Unification algorithm
def unify(x, y, subs):

    x = substitute(x, subs)
    y = substitute(y, subs)

    if x == y:
        return subs

    # If x is a variable
    if is_variable(x):
        subs[x] = y
        return subs

    # If y is a variable
    if is_variable(y):
        subs[y] = x
        return subs

    # If both are function terms
    if isinstance(x, tuple) and isinstance(y, tuple):

        if len(x) != len(y) or x[0] != y[0]:
            return None

        for a, b in zip(x[1:], y[1:]):
            subs = unify(a, b, subs)

            if subs is None:
                return None

        return subs

    return None


# Unify two predicates
def unify_predicate(p1, p2):

    if p1[0] != p2[0]:
        return None

    if len(p1[1]) != len(p2[1]):
        return None

    subs = {}

    for a, b in zip(p1[1], p2[1]):
        subs = unify(a, b, subs)

        if subs is None:
            return None

    return subs


# Main program
print("FIRST ORDER LOGIC - UNIFICATION")

# Example from the lab manual
p1 = ("Eats", ("x", "Apple"))
p2 = ("Eats", ("Riya", "y"))

print("\nExpression 1:", p1)
print("Expression 2:", p2)

result = unify_predicate(p1, p2)

if result is not None:
    print("\nUnification Successful!")
    print("Substitutions:")

    for key, value in result.items():
        print(key, "=", value)

    print("\nUnified Expression: Eats(Riya, Apple)")

else:
    print("\nUnification Failed!")
