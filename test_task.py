# test task 3

from assessment_task_v1 import *

my_circuit = [
{ "gate": "u3", "params": { "theta": 1, "phi": 2, "lambda": -1 }, "target": [0] },
{ "gate": "cx", "target": [0, 1] }
]


# Create ground state vector

my_qpu = get_ground_state(2)


# Run circuit
final_state = run_program(my_qpu, my_circuit)


# Read results

counts = get_counts(final_state, 1000)

print(counts)
