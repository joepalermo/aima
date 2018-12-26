from csp import *

# setup csp
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
csp = CSP(domain_map, constraints)

print(len([c.vars for c in csp.constraints]))
