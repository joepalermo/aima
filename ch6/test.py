from csp import *

def test_ac3():
    # setup csp
    domain_map = {'x': list(range(-10, 10)),
                  'y': list(range(-50, 150))}
    constraints = [Constraint('==', ('x', 'y'))]
    csp = CSP(domain_map, constraints)
    # test
    print(csp.get_domain_volume()) # 4000
    ac3(csp)
    print(csp.get_domain_volume()) # 400
