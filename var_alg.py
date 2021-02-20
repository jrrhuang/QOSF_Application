# Implement variational algorithm

from assessment_task_v1 import *
from scipy import optimize

my_qpu = get_ground_state(3)
my_circuit = [
{ "gate": "u3", "params": { "theta": "global_1", "phi": "global_2", "lambda": -3.1415 }, "target": [0] }
]

def objective_function(params):
    final_state = run_program(my_qpu, my_circuit, { "global_1": params[0], "global_2": params[1] })

    counts = get_counts(final_state, 1000)

    # simple cost function
    cost = 0
    if "000" in counts:
        cost += counts["000"]
    if "100" in counts:
        cost += counts["100"]

    return cost

# initial values
params = np.array([3.1415, 1.5708])

# minimize
minimum = optimize.minimize(objective_function, params, method="Powell", tol=1e-6)

print(minimum)
