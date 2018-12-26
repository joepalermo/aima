def select_unassigned_variable(unassigned_vars, csp):
    return unassigned_vars.pop()

def order_domain_values(var, assignment, csp):
    return csp.domain_map[var]

def test_consistency(assignment, relevant_constraints):
    consistent = True
    for c in relevant_constraints:
        if not test_constraint(c, assignment):
            consistent = False
            break
    return consistent

def test_constraint(constraint, assignment):
    '''return True if the constraint is passed or underdetermined and False otherwise'''
    if constraint.is_binary():
        var1 = constraint.vars[0]
        var2 = constraint.vars[1]
        value1 = assignment.get(var1, None)
        value2 = assignment.get(var2, None)
        if value1 is None or value2 is None:
            return True
        if type(value1) is str:
            value1 = f"\'{value1}\'"
        if type(value2) is str:
            value2 = f"\'{value2}\'"
        return eval(f"{value1} {constraint.op} {value2}")
    else:
        raise Exception("higher-order constraints not yet implemented")
