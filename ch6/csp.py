from operator import mul
from functools import reduce
from copy import copy

class CSP:
    def __init__(self, domain_map, constraints):
        self.vars = set(domain_map.keys())
        self.domain_map = domain_map
        self.constraints = list()
        self.constraint_map = dict()
        for c in constraints:
            # build constraint list
            if c.is_commutative_and_binary():
                self.constraints.extend(mrcc(c))
            else:
                self.constraints.append(c)
            # build constraint map
            for var in c.vars:
                if var not in self.constraint_map:
                    self.constraint_map[var] = [c]
                else:
                    self.constraint_map[var].append(c)

    def get_binary_constraints(self):
        return filter(lambda c: len(c.vars) == 2, self.constraints)

    def get_domain_volume(self):
        return reduce(mul,[len(self.domain_map[var]) for var in self.domain_map], 1)


class Constraint:
    def __init__(self, op, vars):
        self.op = op
        self.vars = vars

    def __hash__(self):
        return hash(self.op + "".join(self.vars))

    def __eq__(self, other):
        return self.op + "".join(self.vars) == other.op + "".join(self.vars)

    def is_binary(self):
        return len(self.vars) == 2

    def is_commutative_and_binary(self):
        return (self.op == '==' or self.op == '!=') and len(self.vars) == 2

def flatten(ls):
    return [item for subls in ls for item in subls]

def mrcc(c):
    'mrcc: make redundant commutative constraint'
    assert len(c.vars) == 2
    return [c, Constraint(c.op, (c.vars[1], c.vars[0]))]

def ac3(csp):
    '''Makes a csp arc-consistent.

    Run-time complexity is: O(c*d*(d^2 + v)), where c is the number of
    constraints, d is the size of the largest domain, and v is the number of
    nodes (or more precisely, the largest number of nodes involved in a binary
    constraint with any node).
    '''
    arc_set = set(csp.get_binary_constraints())
    while len(arc_set) > 0:
        # O(c*d)
        arc = arc_set.pop()
        # revise
        var1, var2 = arc.vars
        # check that each element of the domain of var1 doesn't produce inconsistency
        values_to_remove = list()
        # O(d^2)
        for v in csp.domain_map[var1]:
            satisfied = False
            for w in csp.domain_map[var2]:
                op_string = f'{v} {arc.op} {w}'
                if eval(op_string):
                    satisfied = True
                    break
            if not satisfied:
                values_to_remove.append(v)
        # O(d)
        for v in values_to_remove:
            csp.domain_map[var1].remove(v)
            # test if csp is inconsistent
            if len(csp.domain_map[var1]) == 0:
                return False
        # add more constraints
        # O(v)
        if len(values_to_remove) > 0:
            for c in csp.constraint_map[var1]:
                if c.is_binary() and var1 != c.vars[0]:
                    arc_set.add(c)
    return True


def test_constraint(constraint, assignment):
    '''return True if the constraint is passed or underdetermined and False otherwise'''
    if constraint.is_binary():
        var1 = constraint.vars[0]
        var2 = constraint.vars[1]
        value1 = assignment.get(var1, None)
        value2 = assignment.get(var2, None)
        if value1 is None or value2 is None:
            return True
        return eval(f'{value1} {constraint.op} {value2}')
    else:
        raise Exception("higher-order constraints not yet implemented")

def backtracking_search(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    # if assignment is complete
    if len(assignment) == len(csp.vars):
        return assignment
    unassigned_vars = csp.vars - set(assignment.keys())
    var = select_unassigned_variable(unassigned_vars, csp)
    for v in order_domain_values(var, assignment, csp):
        assignment[var] = v
        associated_constraints = csp.constraint_map[var]
        # test if value is consistent with assignment
        consistent = True
        for c in associated_constraints:
            if not test_constraint(c, assignment):
                consistent = False
                break
        if consistent:
            # inference step
            result = backtrack(assignment, csp)
            if result is not 'failure':
                return result
        del assignment[var]
    return 'failure'

def select_unassigned_variable(unassigned_vars, csp):
    return unassigned_vars.pop()

def order_domain_values(var, assignment, csp):
    return csp.domain_map[var]
