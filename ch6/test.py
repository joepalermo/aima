from csp import *

# setup csp
domain_map = {'x': list(range(-10, 10)),
              'y': list(range(-50, 150))}
constraints = [Constraint('==', ('x', 'y'))]
csp = CSP(domain_map, constraints)

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

test_ac3(csp)
test_backtracking_search(csp)
