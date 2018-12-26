import numpy as np
import math

# general utilitie -------------------------------------------------------------

def get_optimal_indices(values, optimal='min'):
    op = '<' if optimal == 'min' else '>'
    optimal_value = 999 if optimal == 'min' else -999 # fix to inf later
    optimal_indices = []
    for i, value in enumerate(values):
        if eval(f'{value} {op} {optimal_value}'):
            optimal_indices = [i]
        elif value == optimal_value:
            optimal_indices.append(i)
    return optimal_indices

# csp utilities ----------------------------------------------------------------

def naive_select_unassigned_variable(assignment, csp):
    unassigned_vars = csp.vars - set(assignment.keys())
    return unassigned_vars.pop()

def naive_order_domain_values(var, assignment, csp):
    return csp.domain_map[var]

def num_consistent_assignments(var, assignment, csp):
    n_consistent  = 0
    relevant_constraints = csp.constraint_map.get(var, [])
    for v in csp.domain_map[var]:
        assignment[var] = v
        if test_consistency(assignment, relevant_constraints):
            n_consistent += 1
        del assignment[var]
    return n_consistent

def degree_heuristic(var, csp):
    return len(csp.constraint_map[var])

def heuristic_select_unassigned_variable(assignment, csp):
    '''Use minimum-remaining-values (MRV) heuristic to select the next
    unassigned variable, and use the degree heuristic for tie-breaking'''
    unassigned_vars = list(csp.vars - set(assignment.keys()))
    ncas = [num_consistent_assignments(var, assignment, csp) for var in unassigned_vars]
    min_indices = get_optimal_indices(ncas)
    if len(min_indices) == 1:
        return unassigned_vars[min_indices[0]]
    else:
        # tie-breaking needed, use degree heuristic
        vars_to_tie_break = [unassigned_vars[i] for i in min_indices]
        ds = [degree_heuristic(var, csp) for var in vars_to_tie_break]
        min_i = np.argmax(np.array(ds))
        return vars_to_tie_break[min_i]

def heuristic_order_domain_values(var, assignment, csp):
    '''
    Use the least-constraining-value heuristic to select a value for the
    variable currently being assigned.

    currently un-implemented...'''
    return naive_order_domain_values(var, assignment, csp)

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
