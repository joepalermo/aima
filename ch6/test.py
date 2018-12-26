from csp import *

# setup equality csp
domain_map = {'x': list(range(-10, 10)),
              'y': list(range(-50, 150))}
constraints = [Constraint('==', ('x', 'y'))]
equality_csp = CSP(domain_map, constraints)

# setup map colouring csp
domain_map = {'WA': ['r', 'g', 'b'],
              'NT': ['r', 'g', 'b'],
              'SA': ['r', 'g', 'b'],
              'Q': ['r', 'g', 'b'],
              'NSW': ['r', 'g', 'b'],
              'V': ['r', 'g', 'b'],
              'T': ['r', 'g', 'b']}
constraints = [Constraint('!=', ('WA', 'NT')),
               Constraint('!=', ('WA', 'SA')),
               Constraint('!=', ('NT', 'SA')),
               Constraint('!=', ('NT', 'Q')),
               Constraint('!=', ('SA', 'Q')),
               Constraint('!=', ('Q', 'NSW')),
               Constraint('!=', ('SA', 'NSW')),
               Constraint('!=', ('SA', 'V')),
               Constraint('!=', ('V', 'NSW'))]
mc_csp = CSP(domain_map, constraints)

# setup impossible map colouring problem
domain_map = {'WA': ['r', 'g'],
              'NT': ['r', 'g'],
              'SA': ['r', 'g'],
              'Q': ['r', 'g'],
              'NSW': ['r', 'g'],
              'V': ['r', 'g'],
              'T': ['r', 'g']}
impossible_mc_csp = CSP(domain_map, constraints)

def test_ac3(csp):
    # test
    print("testing ac3")
    assert csp.get_domain_volume() == 4000
    ac3(csp)
    assert csp.get_domain_volume() == 400

def test_backtracking_search(csp):
    print("testing backtracking_search")
    result = backtracking_search(csp)
    print(result)

test_ac3(equality_csp)
test_backtracking_search(mc_csp)
test_backtracking_search(impossible_mc_csp)
