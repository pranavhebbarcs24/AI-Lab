import itertools

# Helper functions to identify variables (lowercase) vs constants (Capitalized)
def is_variable(term):
    return isinstance(term, str) and term[0].islower()

def parse_atom(atom_str):
    """Parses 'Predicate(arg1, arg2)' into ('Predicate', ['arg1', 'arg2'])"""
    pred, args = atom_str.strip()[:-1].split('(')
    return pred.strip(), [a.strip() for a in args.split(',')]

def format_atom(pred, args):
    """Formats ('Predicate', ['arg1', 'arg2']) back into 'Predicate(arg1, arg2)'"""
    return f"{pred}({', '.join(args)})"

def substitute(theta, atom):
    """Applies variable substitution dictionary theta to an atomic sentence"""
    pred, args = parse_atom(atom)
    new_args = [theta.get(arg, arg) for arg in args]
    return format_atom(pred, new_args)

def unify(x, y, theta=None):
    """Unifies two atomic sentences or terms, returning a substitution dict or None"""
    if theta is None:
        theta = {}
    if x == y:
        return theta
    if is_variable(x):
        return unify_var(x, y, theta)
    if is_variable(y):
        return unify_var(y, x, theta)
    
    # Unify predicates and their argument lists
    if '(' in x and '(' in y:
        pred_x, args_x = parse_atom(x)
        pred_y, args_y = parse_atom(y)
        if pred_x != pred_y or len(args_x) != len(args_y):
            return None
        for ax, ay in zip(args_x, args_y):
            theta = unify(ax, ay, theta)
            if theta is None:
                return None
        return theta
    return None

def unify_var(var, val, theta):
    if var in theta:
        return unify(theta[var], val, theta)
    if val in theta:
        return unify(var, theta[val], theta)
    new_theta = theta.copy()
    new_theta[var] = val
    return new_theta

def standardize_variables(rule, counter):
    """Replaces variables in a rule with unique ones (e.g., p -> p_1) to avoid clashes"""
    premises, conclusion = rule
    mapping = {}
    
    def rename(atom):
        pred, args = parse_atom(atom)
        new_args = []
        for arg in args:
            if is_variable(arg):
                if arg not in mapping:
                    mapping[arg] = f"{arg}_{next(counter)}"
                new_args.append(mapping[arg])
            else:
                new_args.append(arg)
        return format_atom(pred, new_args)

    return [rename(p) for p in premises], rename(conclusion)

def match_premises(premises, facts, theta=None):
    """Finds all substitutions theta such that all rule premises match known facts"""
    if theta is None:
        theta = {}
    if not premises:
        yield theta
        return
    
    first, rest = premises[0], premises[1:]
    first_sub = substitute(theta, first)
    
    for fact in facts:
        new_theta = unify(first_sub, fact, theta.copy())
        if new_theta is not None:
            yield from match_premises(rest, facts, new_theta)

def fol_fc_ask(facts, rules, query):
    """
    Implementation of FOL-FC-ASK from the slides:
    Iteratively infers new facts until the query is unified or no new facts can be derived.
    """
    kb_facts = list(facts)
    var_counter = itertools.count(1)
    iteration = 1

    # Check if query is already in the initial KB
    for fact in kb_facts:
        phi = unify(fact, query)
        if phi is not None:
            return phi

    while True:
        new_facts = []
        print(f"--- Iteration {iteration} ---")
        
        for rule in rules:
            premises, conclusion = standardize_variables(rule, var_counter)
            
            for theta in match_premises(premises, kb_facts):
                q_prime = substitute(theta, conclusion)
                
                # Check if q_prime already exists in kb_facts or new_facts
                already_known = any(unify(q_prime, f) is not None for f in kb_facts + new_facts)
                if not already_known:
                    new_facts.append(q_prime)
                    print(f"Inferred: {q_prime}  (using {theta})")
                    
                    # Check if the newly inferred fact satisfies the query
                    phi = unify(q_prime, query)
                    if phi is not None:
                        kb_facts.extend(new_facts)
                        return phi

        if not new_facts:
            return False  # No new inferences possible; goal not reached
            
        kb_facts.extend(new_facts)
        iteration += 1

# ==============================================================================
# Knowledge Base Setup (Matching the BMSCE Observation PDF)
# ==============================================================================
if __name__ == "__main__":
    # Initial Atomic Facts (Slide 5)
    initial_facts = [
        "Owns(A, T1)",
        "Missile(T1)",
        "American(Robert)",
        "Enemy(A, America)"
    ]

    # Definite Clauses: (List of Premises, Conclusion) (Slide 5)
    rules = [
        # American(p) ^ Weapon(q) ^ Sells(p, q, r) ^ Hostile(r) => Criminal(p)
        (["American(p)", "Weapon(q)", "Sells(p, q, r)", "Hostile(r)"], "Criminal(p)"),
        
        # Missile(x) ^ Owns(A, x) => Sells(Robert, x, A)
        (["Missile(x)", "Owns(A, x)"], "Sells(Robert, x, A)"),
        
        # Missile(x) => Weapon(x)
        (["Missile(x)"], "Weapon(x)"),
        
        # Enemy(x, America) => Hostile(x)
        (["Enemy(x, America)"], "Hostile(x)")
    ]

    # Goal Query (Slide 5)
    query = "Criminal(Robert)"

    print(f"Initial Facts: {initial_facts}\n")
    print(f"Query: {query}\n")

    result = fol_fc_ask(initial_facts, rules, query)

    print("\n--- Final Result ---")
    if result is not False:
        print(f"SUCCESS: Query '{query}' is PROVEN! (Substitution: {result})")
    else:
        print(f"FAILURE: Query '{query}' could not be proven.")