"""
Run our quantum simulator.
"""

from quantum_simulator_v1 import *

# List of gates in the circuit

my_circuit = [
{ "gate": "h", "target": [0] },
{ "gate": "cx", "target": [0, 1] },
{ "gate": "u3", "params": { "theta": 3.1415, "phi": 1.5708, "lambda": -3.1415 }, "target": [0] }
]

# Input the number of qubits in our "quantum computer"

n = input("Please enter the number of qubits in our simulator: ")
my_qpu = get_ground_state(int(n))

# Run circuit

final_state = run_program(my_qpu, my_circuit)

# Read results

counts = get_counts(final_state, 1000)

print(counts)
