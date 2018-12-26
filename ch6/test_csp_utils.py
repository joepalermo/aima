from csp.utils import *

print("testing get_optimal_indices")
assert [0,1,4] == get_optimal_indices([3, 3, 7, 5, 3], optimal='min')
assert [0,1] == get_optimal_indices([1,1], optimal='min')
assert [0] == get_optimal_indices([1,2], optimal='min')
